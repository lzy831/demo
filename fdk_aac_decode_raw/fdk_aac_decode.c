#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include "aacdecoder_lib.h"

#define DECODER_BUFFSIZE        (2048 * sizeof(INT_PCM))
#define RAW_DATA_BUF_MAX_SIZE   1024
#define MAX_CHANNELS            6

#define AAC_ELD_FILENAME_PATTERN    "../AAC-ELD/dump_%d.raw"
#define AAC_LC_FILENAME_PATTERN     "../AAC-LC/dump_%d.raw"
#define PCM_OUTPUT_FILE_NAME        "./output.pcm"

int g_decode_aac_profile = AOT_ER_AAC_ELD;
unsigned char* g_raw_buf_list[RAW_DATA_BUF_MAX_SIZE];
int g_raw_buf_size_list[RAW_DATA_BUF_MAX_SIZE];
int raw_buf_total_cout = 0;


void prepare_aac_raw_buf_list()
{
  memset(g_raw_buf_list, 0, sizeof(unsigned char*) * RAW_DATA_BUF_MAX_SIZE);
  memset(g_raw_buf_size_list, 0, sizeof(int) * RAW_DATA_BUF_MAX_SIZE);

  char dfilename[64];

  int bread = 0;

  while (1) {
    memset(dfilename, 0, 64);

    if (g_decode_aac_profile == AOT_ER_AAC_ELD) {
      sprintf(dfilename, AAC_ELD_FILENAME_PATTERN, raw_buf_total_cout);
    } else if (g_decode_aac_profile == AOT_AAC_LC) {
      sprintf(dfilename, AAC_LC_FILENAME_PATTERN, raw_buf_total_cout);
    } else {
      exit(1);
    }

    FILE* fp = fopen(dfilename, "rb");
    if (!fp) {
      printf("aac raw buf prepare ok\n");
      break;
    }
    fseek(fp, 0, SEEK_END);
    long rs = ftell(fp);
    // printf("raw_buf_total_cout: %d read file size: %ld\n", raw_buf_total_cout, rs);
    rewind(fp);

    assert(g_raw_buf_list[raw_buf_total_cout] == NULL);
    g_raw_buf_list[raw_buf_total_cout] = (unsigned char*)malloc(sizeof(unsigned char) * rs);
    assert(g_raw_buf_list[raw_buf_total_cout]);
    memset(g_raw_buf_list[raw_buf_total_cout], 0, rs);

    bread = fread(g_raw_buf_list[raw_buf_total_cout], 1, rs, fp);
    assert(bread >= 0);
    g_raw_buf_size_list[raw_buf_total_cout] = bread;
    fclose(fp);

    // printf("process buf idx: %d ok\n", raw_buf_total_cout);
    raw_buf_total_cout++;
  }
}

void release_aac_raw_buf_list()
{
  for (int i = 0; i < RAW_DATA_BUF_MAX_SIZE; i++) {
    if (g_raw_buf_list[i]) {
      free(g_raw_buf_list[i]);
    }
  }
}


int main()
{
  AAC_DECODER_ERROR err = AAC_DEC_OK;
  HANDLE_AACDECODER decoder = aacDecoder_Open(TT_MP4_RAW, 1);
  assert(decoder);

  // 设置ASC信息
  if (g_decode_aac_profile == AOT_ER_AAC_ELD) {
    UCHAR conf[] = {0xF8, 0xF0, 0x20, 0x00};  //AAL-ELD 16000kHz MONO
    UCHAR* conf_array[1] = { conf };
    UINT length = 4;
    err = aacDecoder_ConfigRaw(decoder, conf_array, &length);
    assert(!err);
  } else if (g_decode_aac_profile == AOT_AAC_LC) {
    UCHAR conf[] = {0x12, 0x10};  //AAL-LC 44100kHz STEREO
    UCHAR* conf_array[1] = { conf };
    UINT length = 2;
    err = aacDecoder_ConfigRaw(decoder, conf_array, &length);
    assert(!err);
  }

  // 获取信息
  CStreamInfo* info = aacDecoder_GetStreamInfo(decoder);
  assert(info);
  // printf("aacSampleRate: %d\n", info->aacSampleRate);
  // printf("channelConfig: %d\n", info->channelConfig);
  // printf("aot: %d\n", info->aot);

  // 构建AAC Raw Data Buffer List
  prepare_aac_raw_buf_list();


  // pcm输出buffer的大小可以参考CStreamInfo中frameSize的定义
  // typedef struct {
  // ...
  //   INT frameSize;  /*!< The frame size of the decoded PCM audio signal. \n
  //                        Typically this is: \n
  //                        1024 or 960 for AAC-LC \n
  //                        2048 or 1920 for HE-AAC (v2) \n
  //                        512 or 480 for AAC-LD and AAC-ELD \n
  //                        768, 1024, 2048 or 4096 for USAC  */
  //...
  //}CStreamInfo
  int max_frame_size;
  if (g_decode_aac_profile == AOT_ER_AAC_ELD) {
    max_frame_size = 512;
  } else if (g_decode_aac_profile == AOT_AAC_LC) {
    max_frame_size = 1024;
  }

  int pcm_buffer_size = max_frame_size * MAX_CHANNELS;
  INT_PCM* pcm_buffer = (INT_PCM*)malloc(sizeof(INT_PCM) * pcm_buffer_size);
  assert(pcm_buffer);

  FILE* output_fp = fopen(PCM_OUTPUT_FILE_NAME, "wb");
  assert(output_fp);


  // 开始解码循环
  int cur_raw_buf_index = 0;
  UINT flags = 0;
  UINT bytes_valid;
  do {

    if (cur_raw_buf_index >= raw_buf_total_cout) {
      printf("decode end\n");
      break;
    }

    // 加载本次需要解码的数据
    bytes_valid = g_raw_buf_size_list[cur_raw_buf_index];
    err = aacDecoder_Fill(decoder, &(g_raw_buf_list[cur_raw_buf_index]), &(g_raw_buf_size_list[cur_raw_buf_index]), &bytes_valid);
    assert(err == AAC_DEC_OK);

    // 解码
    err = aacDecoder_DecodeFrame(decoder, pcm_buffer, pcm_buffer_size / sizeof(INT_PCM), flags);
    // 因为这里我们解码的是Raw Data，每次送入一帧后就可以解码完成返回AAC_DEC_OK
    // 对于非Raw Data 的情况需要针对返回值进行处理，如出错处理，数据不够的处理
    assert(err == AAC_DEC_OK);

    // 通过获取信息，计算实际输出的pcm数据大小
    CStreamInfo* info = aacDecoder_GetStreamInfo(decoder);
    assert(info);
    // printf("sampleRate: %d\n", info->sampleRate);
    // printf("frameSize: %d\n", info->frameSize);
    // printf("numChannels: %d\n", info->numChannels);
    int output_pcm_bytes = info->frameSize * info->numChannels * 2;

    // pcm 数据写入文件
    if (output_fp) {
      size_t ws = fwrite(pcm_buffer, output_pcm_bytes, 1, output_fp);
      assert(ws > 0);
    }

    cur_raw_buf_index++;
  } while (1);

  // 释放资源
  if (output_fp) {
    fclose(output_fp);
  }
  if (pcm_buffer) {
    free(pcm_buffer);
  }
  release_aac_raw_buf_list();

  return 0;
}