from main.model.rtp.RTPHeader import RTPHeader
from main.model.rtp.RTPPayload import RTPPayload


class SRTPAuthMessage:
    
    # The payload of the SRTP Packet
    payload: RTPPayload
    
    # The SRTP Header is based on the RTP one
    header: RTPHeader
    