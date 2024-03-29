from src.main.model.rtcp.RTCPConsts import REPORT_BLOCK_SIZE
from src.main.model.rtcp.RTCPHeader import RTCPHeader
from src.main.model.rtcp.r.RTCPReportBlock import RTCPReportBlock
from src.main.model.rtcp.sr.RTCPSRSenderInfo import RTCPSRSenderInfo

class RTCPSRPacket:
    
    def to_bytes(self) -> bytearray:
        
        raw_reports_block = bytearray(REPORT_BLOCK_SIZE * len(self.reports))
        
        for report_index in range(len(self.reports)):
            
            raw_reports_block[report_index * REPORT_BLOCK_SIZE: (report_index + 1) * REPORT_BLOCK_SIZE] = self.reports[report_index].to_bytes()
        
        return self.header.to_bytes() + self.sender_info.to_bytes() + raw_reports_block + self.profil_specific_data
    
    #Header part
    header: RTCPHeader
    
    #First Mandatory part of SR Packet
    sender_info: RTCPSRSenderInfo
    
    #List of sender report blocks
    reports: list[RTCPReportBlock]
    
    # A profile-specific extension may be added
    # (must be 32 bits blocks)
    profil_specific_data : bytearray = bytearray()