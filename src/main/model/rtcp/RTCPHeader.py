from main.model.rtcp.RTCPSimpleHeader import RTCPSimpleHeader


class RTCPHeader(RTCPSimpleHeader):
    
    def __init__(self, parent: RTCPSimpleHeader = None) -> None:
        super().__init__()
        if parent is not None:
            self.version = parent.version
            self.block_count = parent.block_count
            self.length = parent.length
            self.marker = parent.marker
            self.padding = parent.padding
            self.payload_type = parent.payload_type
    
    def to_bytes(self) -> bytearray:
        
        return super().to_bytes() + self.ssrc.to_bytes(4)
        
    # SSRC synchronized source on 32 bits
    ssrc: int 