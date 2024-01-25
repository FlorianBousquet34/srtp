from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.sdes.RTCPSDESChunk import RTCPSDEChunk


class RTCPSDESPacket:
    
    header : RTCPHeader
    
    chuncks : list[RTCPSDEChunk]