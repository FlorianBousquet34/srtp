from main.model.rtcp.RTCPConsts import REPORT_BLOCK_SIZE
from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.r.RTCPReportBlock import RTCPReportBlock


class RTCPRRPacket:
    
    def to_bytes(self) -> bytearray:
        
        raw_reports_block = bytearray(REPORT_BLOCK_SIZE * len(self.reports))
        
        for report_index in range(len(self.reports)):
            
            raw_reports_block[report_index * REPORT_BLOCK_SIZE: (report_index + 1) * REPORT_BLOCK_SIZE] = self.reports[report_index].to_bytes()
        
        return self.header.to_bytes() + raw_reports_block + self.profil_specific_data
    
    #Header part
    header: RTCPHeader
    
    #List of report blocks
    reports: list[RTCPReportBlock]
    
    # A profile-specific extension may be added
    profil_specific_data : bytearray