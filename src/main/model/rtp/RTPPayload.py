class RTPPayload:
    
    # The size of the padding
    pad_count: int
    
    # The padded payload
    raw_payload: bytearray
    
    # Payload message without paddin
    payload: str
    
    
    