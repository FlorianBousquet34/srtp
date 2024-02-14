from src.main.model.rtcp.RTCPSimpleHeader import RTCPSimpleHeader
from src.main.model.rtcp.sdes.RTCPSDESChunk import RTCPSDEChunk


class RTCPSDESPacket:
    
    def to_bytes(self) -> bytearray:
        
        raw_chuncks = bytearray()
        for chunk_index in range(len(self.chuncks)):
            
            raw_chuncks += self.chuncks[chunk_index].to_bytes()
        
        return self.header.to_bytes() + raw_chuncks
    
    header : RTCPSimpleHeader
    
    chuncks : list[RTCPSDEChunk]