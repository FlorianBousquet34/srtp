from main.model.rtp.RTPHeader import RTPHeader
from main.model.rtp.RTPPayload import RTPPayload


class RTPPacket:
    
    def __init__(self, raw_data: bytearray) -> None:
        
        self.raw_data = raw_data
    
    # The RTP Header
    header: RTPHeader
    
    # The RTP Payload
    payload: RTPPayload
    
    raw_data: bytearray