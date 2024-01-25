from main.model.rtcp.r.RTCPRHeader import RTCPRHeader
from main.model.rtcp.r.RTCPReportBlock import RTCPReportBlock


class RTCPRRPacket:
    
    #Header part
    header: RTCPRHeader
    
    #List of report blocks
    reports: list[RTCPReportBlock]
    
    # A profile-specific extension may be added