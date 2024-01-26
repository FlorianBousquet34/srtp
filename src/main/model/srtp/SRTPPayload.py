from main.model.rtp.RTPPayload import RTPPayload


class SRTPPaylaod:
    
    # The original encrypted paylaod
    encrypted_payload: bytearray
    
    # The decypted payload
    decrypted_payload: RTPPayload