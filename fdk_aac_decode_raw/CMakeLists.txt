cmake_minimum_required (VERSION 2.8.7)
project (fdk_aac_decode)

# https://downloads.sourceforge.net/opencore-amr/fdk-aac-2.0.0.tar.gz
# $ ./configure
# $ make
# $ sudo make install
SET(FDKAAC_SOURCE_PATH "/home/lzy/external_library/fdk-aac-2.0.0")
FIND_LIBRARY(FDKAAC_LIB fdk-aac  ${FDKAAC_SOURCE_PATH}/.libs/ NO_CMAKE_FIND_ROOT_PATH)
# set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g")

include_directories(
  ${FDKAAC_SOURCE_PATH}/libAACdec/include
  ${FDKAAC_SOURCE_PATH}/libSYS/include
  )

add_executable(fdk_aac_decode fdk_aac_decode.c)
target_link_libraries(fdk_aac_decode ${FDKAAC_LIB})