from main.model.rtcp.R.RTCPRHeader import RTCPRHeader
from main.model.rtcp.R.RTCPReportBlock import RTCPReportBlock
from main.model.rtcp.SR.RTCPSRSenderInfo import RTCPSRSenderInfo


class RTCPSRPacket:
    
    #Header part
    header: RTCPRHeader
    
    #First Mandatory part of SR Packet
    senderInfo: RTCPSRSenderInfo
    
    #List of sender report blocks
    reports: list[RTCPReportBlock]
    
    # A profile-specific extension may be added
    