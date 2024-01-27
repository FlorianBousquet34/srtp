from main.model.rtcp.RTCPHeader import RTCPHeader


class RTCPAPPPacket:
    
    # App packet is for experiment use when building new apps
    
    header : RTCPHeader
    
    # 32 bits ASCII name
    name: str
    
    # application relative date
    # variable length multiple of 32 bits
    data : bytearray