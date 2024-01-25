from main.model.rtcp.R.RTCPRHeader import RTCPRHeader
from main.model.rtcp.R.RTCPReportBlock import RTCPReportBlock


class RTCPRRPacket:
    
    #Header part
    header: RTCPRHeader
    
    #List of report blocks
    reports: list[RTCPReportBlock]
    
    # A profile-specific extension may be added