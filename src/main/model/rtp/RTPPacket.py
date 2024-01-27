from main.model.rtp.RTPHeader import RTPHeader
from main.model.rtp.RTPPayload import RTPPayload


class RTPPacket:
    
    def __init__(self, raw_packet: bytearray) -> None:
        
        self.raw_packet = raw_packet
    
    # The RTP Header
    header: RTPHeader
    
    # The RTP Payload
    payload: RTPPayload
    
    raw_packet: bytearray