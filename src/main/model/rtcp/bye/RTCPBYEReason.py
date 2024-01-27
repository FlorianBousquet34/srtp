from main.utils.transformer.PaddingUtils import PaddingUtils


class RTCPBYEReason:
    
    def to_bytes(self) -> bytearray:
        
        if self.reason is not None and self.reason != "":
            
            _ , payload, self.length = PaddingUtils.pad_string(self.reason)
        
        return payload
    
    length: int
    
    reason: str