from main.model.rtp.RTPHeader import RTPHeader
from main.model.rtp.RTPPayload import RTPPayload


class RTPPacket:
    
    def __init__(self, raw_data: bytearray) -> None:
        
        self.raw_data = raw_data
        
    def to_bytes(self) -> bytearray:
        
        self.raw_data = self.header.to_bytes() + self.payload.to_bytes()
        
        return self.raw_data
    
    # The RTP Header
    header: RTPHeader
    
    # The RTP Payload
    payload: RTPPayload
    
    raw_data: bytearray