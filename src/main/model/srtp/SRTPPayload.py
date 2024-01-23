from main.model.rtp.RTPPayload import RTPPayload


class SRTPPaylaod:
    
    # The original encrypted paylaod
    encryptedPayload: bytearray
    
    # The decypted payload
    decryptedPayload: RTPPayload