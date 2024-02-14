from src.main.utils.transformer.PaddingUtils import PaddingUtils


class RTPPayload:
    
    def to_bytes(self) -> bytearray:
        
        _, self.raw_payload, self.pad_count = PaddingUtils.pad_string(self.payload)
        
        return self.raw_payload
    
    # The size of the padding
    pad_count: int
    
    # The padded payload
    raw_payload: bytearray
    
    # Payload message without paddin
    payload: str