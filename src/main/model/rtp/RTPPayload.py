class RTPPayload:
    
    # The size of the padding
    padCount: int
    
    # The padded payload
    rawPayload: bytearray
    
    # Payload message without paddin
    payload: str
    
    
    