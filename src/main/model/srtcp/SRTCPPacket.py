from src.main.model.rtcp.RTCPConsts import IS_ENCRYPTED_MULTIPLIER
from src.main.model.rtcp.RTCPPacket import RTCPPacket

class SRTCPPacket(RTCPPacket):
    
    def __init__(self, parent: RTCPPacket = None) -> None:
        super().__init__()
        if parent is not None:
            self.packet = parent.packet
            self.raw_data = parent.raw_data
    
    def to_bytes(self) -> bytearray:
        
        self.raw_data = self.packet.to_bytes()
        
        # compute length
        # 32-bits word of payload - one - (srtp index + is_encrypted (32 bits))
        self.packet.header.length = len(self.raw_data) // 4 - 2
        self.raw_data[2:4] = self.packet.header.length.to_bytes(2)
        
        return super().to_bytes() + (self.is_encrypted * IS_ENCRYPTED_MULTIPLIER + self.srtcp_index).to_bytes(4)
    
    # Whether this particular SRTCP Packet is encrypted or not
    is_encrypted: bool = True
    
    # the index of the current srtcp packet on 31 bits
    srtcp_index: int
    
    