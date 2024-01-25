from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.bye.RTCPBYEReason import RTCPBYEReason


class RTCPBYEPacket:
    
    header : RTCPHeader
    
    # source of the bye packet
    sources : list[int]
    
    # opt reason of leaving
    reason : RTCPBYEReason | None