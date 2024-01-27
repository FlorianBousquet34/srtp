from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.r.RTCPReportBlock import RTCPReportBlock


class RTCPRRPacket:
    
    #Header part
    header: RTCPHeader
    
    #List of report blocks
    reports: list[RTCPReportBlock]
    
    # A profile-specific extension may be added
    profil_specific_data : bytearray