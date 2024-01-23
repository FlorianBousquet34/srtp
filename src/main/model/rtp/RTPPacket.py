from main.model.rtp.RTPHeaderExtension import RTPHeaderExtension
from main.model.rtp.RTPPayload import RTPPayload


class RTPPacket:
    
    header: RTPHeaderExtension
    
    payload: RTPPayload