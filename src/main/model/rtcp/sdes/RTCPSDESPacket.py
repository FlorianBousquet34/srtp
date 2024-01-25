from main.model.rtcp.r.RTCPRHeader import RTCPRHeader
from main.model.rtcp.sdes.RTCPSDESChunk import RTCPSDEChunk


class RTCPSDESPacket:
    
    header : RTCPRHeader
    
    chuncks : list[RTCPSDEChunk]