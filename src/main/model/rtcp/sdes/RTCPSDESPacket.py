from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.sdes.RTCPSDESChunk import RTCPSDEChunk


class RTCPSDESPacket:
    
    def to_bytes(self) -> bytearray:
        
        raw_chuncks = bytearray()
        for chunk_index in range(len(self.chuncks)):
            
            raw_chuncks.append(self.chuncks[chunk_index].to_bytes())
            
        return self.header.to_bytes() + raw_chuncks[4:]
    
    header : RTCPHeader
    
    chuncks : list[RTCPSDEChunk]