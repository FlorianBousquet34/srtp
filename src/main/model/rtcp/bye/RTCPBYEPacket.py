from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.bye.RTCPBYEReason import RTCPBYEReason


class RTCPBYEPacket:
    
    def to_bytes(self) -> bytearray:
        
        # compute reason bytes if present
        raw_reason = bytearray(0)
        if self.reason is not None:
            raw_reason = self.reason.to_bytes()
        
        # compute sources to bytes
        # first source is included in header
        sources_bytes = bytearray(len(self.sources - 1))
        for index in range(len(self.sources - 1)):
            sources_bytes[index] = self.sources[index].to_bytes()
 
        return self.header.to_bytes() + sources_bytes + raw_reason
    
    header : RTCPHeader
    
    # source of the bye packet
    sources : list[int]
    
    # opt reason of leaving
    reason : RTCPBYEReason | None