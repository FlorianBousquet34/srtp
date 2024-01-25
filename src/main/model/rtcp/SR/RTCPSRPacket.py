from main.model.rtcp.SR.RTCPSRHeader import RTCPSRHeader
from main.model.rtcp.SR.RTCPSRReportBlock import RTCPSRReportBlock
from main.model.rtcp.SR.RTCPSRSenderInfo import RTCPSRSenderInfo


class RTCPSRPacket:
    
    #Header part
    header: RTCPSRHeader
    
    #First Mandatory part of SR Packet
    senderInfo: RTCPSRSenderInfo
    
    #List of sender report blocks
    reports: list[RTCPSRReportBlock]
    
    # A profile-specific extension may be added
    