from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.r.RTCPReportBlock import RTCPReportBlock
from main.model.rtcp.sr.RTCPSRSenderInfo import RTCPSRSenderInfo


class RTCPSRPacket:
    
    #Header part
    header: RTCPHeader
    
    #First Mandatory part of SR Packet
    sender_info: RTCPSRSenderInfo
    
    #List of sender report blocks
    reports: list[RTCPReportBlock]
    
    # A profile-specific extension may be added
    