from src.main.model.rtcp.RTCPHeader import RTCPHeader
from src.main.utils.transformer.PaddingUtils import PaddingUtils


class RTCPAPPPacket:
    
    def to_bytes(self) -> bytearray:
        
        _, name_data, _ = PaddingUtils.pad_string(self.name)
        
        return self.header.to_bytes() + name_data + self.data
    
    # App packet is for experiment use when building new apps
    
    header : RTCPHeader
    
    # 32 bits ASCII name
    name: str
    
    # application relative date
    # variable length multiple of 32 bits
    data : bytearray