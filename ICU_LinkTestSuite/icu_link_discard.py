BIT_SYN = 7
BIT_ACK = 6
BIT_EAK = 5
BIT_RST = 4
BIT_NAK = 3
BIT_RES2 = 2
BIT_RES1 = 1
BIT_RES0 = 0
LINK_PKT_MAX_PSN = 255


LinkPacketSYNLength = 2
LinkPacketHeaderLength = 10
LinkPacketHeaderFormat = '>HHBBBBH'
LinkPacketHeaderWithoutChecksumFormat = '>HHBBBB'
LinkPacketHeaderField = 'StartOfPacket, PacketLength, ControlByte, PacketSeqNum, PacketAckNum, SessionId, HeaderChecksum'
LinkPacketHeaderTupleType = namedtuple(
    'LinkPacketHeaderTuple', LinkPacketHeaderField)

LinkSynPayloadLength = 12
LinkSynPayloadFormat = '>BBHHHBBH'
LinkSynPayloadWithoutCheckssumFormat = '>BBHHHBB'
LinkSynPayloadField = 'LinkVersion, MaxNumOfOutStdPkts, MaxRecvPktLen, RetransTimeout, CumAckTimeout, MaxNumOfRetrans, MaxCumAck, PayloadChecksum'
LinkSynPayloadTupleType = namedtuple(
    'LinkSynPayloadTuple', LinkSynPayloadField)

Valid_SYN_Header_Param = dict(
    SYN=1, ACK=0, EAK=0, RST=0, NAK=0, RES1=0, RES2=0, RES3=0,
    PacketLength=LinkPacketHeaderLength+LinkSynPayloadLength)
Valid_RST_Header_param = dict(
    SYN=0, ACK=0, EAK=0, RST=1, NAK=0, RES1=0, RES2=0, RES3=0,
    PacketLength=LinkPacketHeaderLength)
Valid_ACK_Header_Param = dict(
    ACK=1, EAK=0, RST=0, NAK=0, RES1=0, RES2=0, RES3=0,)


MCU_Default_SYN_Param = dict()
MCU_Negotiated_SYN_Param = dict()


def is_valid_packet_header(header_data: bytes):
    return True


def is_valid_syn_or_syn_ack_packet(header: LinkPacketHeaderTupleType):
    # skdebug('header.ControlByte:', bin(header.ControlByte))
    # skdebug('1<<BIT_SYN:', bin(1 << BIT_SYN))
    return header.ControlByte == 1 << BIT_SYN or header.ControlByte == (1 << BIT_SYN | 1 << BIT_ACK)


def is_reset_packet(packet: bytes):
    header_bytes = packet[:10]
    debug_header(header_bytes)
    header = LinkPacketHeaderTupleType._make(
        struct.unpack(LinkPacketHeaderFormat, header_bytes))
    return header.ControlByte == 1 << BIT_RST


def get_syn_param(payload_bytes: bytes):
    skdebug('payload_bytes len:', len(payload_bytes))
    payload = LinkSynPayloadTupleType._make(
        struct.unpack(LinkSynPayloadFormat, payload_bytes))
    syn_param = dict(
        LinkVersion=payload.LinkVersion,
        MaxNumOfOutStdPkts=payload.MaxNumOfOutStdPkts,
        MaxRecvPktLen=payload.MaxRecvPktLen,
        RetransTimeout=payload.RetransTimeout,
        CumAckTimeout=payload.CumAckTimeout,
        MaxNumOfRetrans=payload.MaxNumOfRetrans,
        MaxCumAck=payload.MaxCumAck)
    return syn_param


def get_packet_param(packet: bytes):
    header_bytes = packet[:10]
    skdebug('header_bytes len:', len(header_bytes))
    header = LinkPacketHeaderTupleType._make(
        struct.unpack(LinkPacketHeaderFormat, header_bytes))
    header_param = dict(PacketLength=header.PacketLength,
                        SYN=(header.ControlByte & 1 << BIT_SYN) >> BIT_SYN,
                        ACK=(header.ControlByte & 1 << BIT_ACK) >> BIT_ACK,
                        EAK=(header.ControlByte & 1 << BIT_EAK) >> BIT_EAK,
                        RST=(header.ControlByte & 1 << BIT_RST) >> BIT_RST,
                        NAK=(header.ControlByte & 1 << BIT_NAK) >> BIT_NAK,
                        PacketSeqNum=header.PacketSeqNum,
                        PacketAckNum=header.PacketAckNum,
                        SessionId=header.SessionId)
    skdebug(header_param)
    if is_valid_syn_or_syn_ack_packet(header):
        # skdebug('is valid syn packet')
        syn_payload_param = get_syn_param(packet[10:])
        return {**header_param, **syn_payload_param}
    else:
        skdebug('is not valid syn packet')
        return header_param


def get_payload_len_from_header(header_data: bytes):
    header = LinkPacketHeaderTupleType._make(
        struct.unpack(LinkPacketHeaderFormat, header_data))
    return header.PacketLength-LinkPacketHeaderLength


def debug_header(header_data: bytes):
    header = LinkPacketHeaderTupleType._make(
        struct.unpack(LinkPacketHeaderFormat, header_data))

    # print(header)
    skdebug(header)
    skdebug("ControlByte:", bin(header.ControlByte))

    # skdebug("StartOfPacket:", hex(header.StartOfPacket))
    # skdebug("PacketLength:", header.PacketLength)
    # skdebug("ControlByte:", format(header.ControlByte, 'b'))
    # skdebug("PacketSeqNum:", header.PacketSeqNum)
    # skdebug("PacketAckNum:", header.PacketAckNum)
    # skdebug("SessionId:", header.SessionId)
    # skdebug("HeaderChecksum:", hex(header.HeaderChecksum))


def debug_syn_payload(payload_data: bytes):
    skdebug('payload_data len', len(payload_data))
    payload = LinkSynPayloadTupleType._make(
        struct.unpack(LinkSynPayloadFormat, payload_data))
    skdebug(payload)


def clac_checksum(data_without_checksum: bytes):
    skdebug('clac_checksum begin, data:', data_without_checksum.hex())
    checksum = 0
    for value in data_without_checksum:
        checksum = checksum + value
        # skdebug('checksum', hex(checksum), 'value', value)
    return checksum


def generate_syn_payload_with_param(**param):
    skdebug('generate_syn_payload_with_param')
    skdebug('param:', param)
    # for name, value in param.items():
    #     skdebug('name:', name, 'value:', value)
    LinkVersion = int(param.get('LinkVersion', 0x1))
    MaxNumOfOutStdPkts = int(param.get('MaxNumOfOutStdPkts', 0))
    MaxRecvPktLen = int(param.get('MaxRecvPktLen', 0))
    RetransTimeout = int(param.get('RetransTimeout', 0))
    CumAckTimeout = int(param.get('CumAckTimeout', 0))
    MaxNumOfRetrans = int(param.get('MaxNumOfRetrans', 0))
    MaxCumAck = int(param.get('MaxCumAck', 0))

    # calc payload checksum
    data_without_checksum = struct.pack(LinkSynPayloadWithoutCheckssumFormat, LinkVersion, MaxNumOfOutStdPkts,
                                        MaxRecvPktLen, RetransTimeout, CumAckTimeout, MaxNumOfRetrans, MaxCumAck)
    checksum = clac_checksum(data_without_checksum)
    PayloadChecksum = int(param.get('PayloadChecksum', checksum))
    return struct.pack(
        LinkSynPayloadFormat, LinkVersion, MaxNumOfOutStdPkts, MaxRecvPktLen, RetransTimeout, CumAckTimeout,
        MaxNumOfRetrans, MaxCumAck, PayloadChecksum)


def generate_standard_SYN_ACK_packet(**param):
    global MCU_Default_SYN_Param
    syn_ack_param = dict()
    syn_ack_param['MaxNumOfOutStdPkts'] = int(MCU_Default_SYN_Param.get('MaxNumOfOutStdPkts', 4))
    syn_ack_param['MaxRecvPktLen'] = int(MCU_Default_SYN_Param.get('MaxRecvPktLen', 256))
    syn_ack_param['RetransTimeout'] = int(MCU_Default_SYN_Param.get('RetransTimeout', 400))
    syn_ack_param['CumAckTimeout'] = int(param.get('CumAckTimeout', 22))
    syn_ack_param['MaxNumOfRetrans'] = int(param.get('MaxNumOfRetrans', 10))
    syn_ack_param['MaxCumAck'] = int(param.get('MaxCumAck', 10))
    payload = generate_syn_payload_with_param(**syn_ack_param)
    pkt_len = LinkSynPayloadLength+LinkPacketHeaderLength
    header_param = dict(SYN=1, ACK=1, PacketLength=pkt_len)
    header_param['PacketSeqNum'] = int(param.get('PacketSeqNum', 0))
    header_param['PacketAckNum'] = int(param.get('PacketAckNum', 0))
    header = generate_header_with_param(**header_param)
    packet = header+payload
    return packet


def generate_negotiated_SYN_ACK_packet(**param):
    global MCU_Default_SYN_Param
    syn_ack_param = dict()
    syn_ack_param['MaxNumOfOutStdPkts'] = int(MCU_Default_SYN_Param.get('MaxNumOfOutStdPkts', 4))
    syn_ack_param['MaxRecvPktLen'] = int(MCU_Default_SYN_Param.get('MaxRecvPktLen', 256))
    syn_ack_param['RetransTimeout'] = int(MCU_Default_SYN_Param.get('RetransTimeout', 400))
    syn_ack_param['CumAckTimeout'] = int(param.get('CumAckTimeout', 22))
    # 修改可协商参数MaxNumOfRetrans值用以到达再次协商的目的
    # syn_ack_param['MaxNumOfRetrans'] = int(param.get('MaxNumOfRetrans', 10)) # + int(2)
    syn_ack_param['MaxCumAck'] = int(param.get('MaxCumAck', 10))
    payload = generate_syn_payload_with_param(**syn_ack_param)
    pkt_len = LinkSynPayloadLength+LinkPacketHeaderLength
    header_param = dict(SYN=1, ACK=1, PacketLength=pkt_len)
    header_param['PacketSeqNum'] = int(param.get('PacketSeqNum', 0))
    header_param['PacketAckNum'] = int(param.get('PacketSeqNum', 0))
    header = generate_header_with_param(**header_param)
    packet = header+payload
    return packet


def generate_nak_payload_with_param(**param):
    skdebug('generate_nak_payload_with_param')
    len = param.get('len', 10)
    data_without_checksum = bytearray()
    for i in range(len):
        data_without_checksum.append(i)
    skdebug('data_without_checksum:', data_without_checksum.hex())
    checksum = clac_checksum(data_without_checksum)
    payload = data_without_checksum + struct.pack('>H', checksum)
    skdebug('payload:', payload.hex())
    return payload


def generate_header_with_param(**param):
    skdebug('generate_syn_header_with_param')
    # header = get_default_header_bytes_array()
    StartOfPacket = param.get('StartOfPacket', 0xAA55)
    PacketLength = param.get('PacketLength', 0)

    # ControlByte = BitSet(8)
    # ControlByte.reset()
    # if param.get('SYN', 0) == 1:
    #     ControlByte.set(BIT_SYN)
    # if param.get('ACK', 0) == 1:
    #     ControlByte.set(BIT_ACK)
    # if param.get('EAK', 0) == 1:
    #     ControlByte.set(BIT_EAK)
    # if param.get('RST', 0) == 1:
    #     ControlByte.set(BIT_RST)
    # if param.get('NAK') == 1:
    #     ControlByte.set(BIT_NAK)
    # if param.get('RES1') == 1:
    #     ControlByte.set(BIT_RES2)
    # if param.get('RES2') == 1:
    #     ControlByte.set(BIT_RES1)
    # if param.get('RES3') == 1:
    #     ControlByte.set(BIT_RES0)
    ControlByte = 0
    if param.get('SYN', 0) == 1:
        ControlByte = ControlByte | (1 << BIT_SYN)
    if param.get('ACK', 0) == 1:
        ControlByte = ControlByte | (1 << BIT_ACK)
    if param.get('EAK', 0) == 1:
        ControlByte = ControlByte | (1 << BIT_EAK)
    if param.get('RST', 0) == 1:
        ControlByte = ControlByte | (1 << BIT_RST)
    if param.get('NAK') == 1:
        ControlByte = ControlByte | (1 << BIT_NAK)
    if param.get('RES1') == 1:
        ControlByte = ControlByte | (1 << BIT_RES2)
    if param.get('RES2') == 1:
        ControlByte = ControlByte | (1 << BIT_RES1)
    if param.get('RES3') == 1:
        ControlByte = ControlByte | (1 << BIT_RES0)

    skdebug('ControlByte:', bin(ControlByte))

    PacketSeqNum = param.get('PacketSeqNum', 0)
    PacketAckNum = param.get('PacketAckNum', 0)
    SessionId = param.get('SessionId', 0)

    data_without_checksum = struct.pack(LinkPacketHeaderWithoutChecksumFormat, StartOfPacket,
                                        PacketLength, ControlByte, PacketSeqNum, PacketAckNum, SessionId)
    checksum = clac_checksum(data_without_checksum)
    HeaderChecksum = param.get('HeaderChecksum', checksum)

    return struct.pack(
        LinkPacketHeaderFormat, StartOfPacket, PacketLength, ControlByte, PacketSeqNum, PacketAckNum, SessionId,
        HeaderChecksum)