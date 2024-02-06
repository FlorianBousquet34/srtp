from main.model.rtp.RTPHeader import RTPHeader
from main.model.rtp.RTPPayload import RTPPayload


class RTPPacket:
    
    def __init__(self, raw_data: bytearray | None = None) -> None:
        
        if raw_data:
            self.raw_data = raw_data
        
    def to_bytes(self) -> bytearray:
        
        self.payload.to_bytes()
        
        if self.payload.pad_count > 0:
            self.header.fixed_header.padding = True
        
        self.raw_data = self.header.to_bytes() + self.payload.raw_payload
        
        return self.raw_data
    
    # The RTP Header
    header: RTPHeader
    
    # The RTP Payload
    payload: RTPPayload
    
    raw_data: bytearray