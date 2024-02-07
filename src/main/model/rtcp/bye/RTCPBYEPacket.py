from main.model.rtcp.RTCPSimpleHeader import RTCPSimpleHeader
from main.model.rtcp.bye.RTCPBYEReason import RTCPBYEReason


class RTCPBYEPacket:
    
    def to_bytes(self) -> bytearray:
        
        # compute reason bytes if present
        raw_reason = bytearray(0)
        if self.reason is not None:
            raw_reason = self.reason.to_bytes()
        
        # compute sources to bytes
        sources_bytes = bytearray(len(self.sources) * 4)
        for index in range(len(self.sources)):
            sources_bytes[index * 4: (index + 1) * 4] = self.sources[index].to_bytes(4)
 
        return self.header.to_bytes() + sources_bytes + raw_reason
    
    header : RTCPSimpleHeader
    
    # source of the bye packet
    sources : list[int]
    
    # opt reason of leaving
    reason : RTCPBYEReason | None