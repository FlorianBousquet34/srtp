from src.main.utils.transformer.PaddingUtils import PaddingUtils


class RTCPBYEReason:
    
    def to_bytes(self) -> bytearray:
        
        if self.reason is not None and self.reason != "":
            
            self.length = len(self.reason)
            pad_count = 4 - ((self.length + 1) % 4)
        
        return self.length.to_bytes() + self.reason.encode() + bytearray(pad_count)
    
    length: int
    
    reason: str