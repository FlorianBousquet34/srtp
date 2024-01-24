from main.model.rtp.RTPHeader import RTPHeader
from main.model.rtp.RTPPayload import RTPPayload


class RTPPacket:
    
    # The RTP Header
    header: RTPHeader
    
    # The RTP Payload
    payload: RTPPayload
    
    rawPacket: bytearray