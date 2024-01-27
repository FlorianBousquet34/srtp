from main.model.rtcp.sdes.items.RTCPGenericItem import RTCPGenericItem
from main.utils.transformer.PaddingUtils import PaddingUtils


class RTCPSDEChunk:
    
    def to_bytes(self) -> bytearray:
        
        raw_items = bytearray()
        
        for sdes_index in range(len(self.sdes_items)):
            
            raw_items.append(self.sdes_items[sdes_index].to_bytes())
        
        return self.source.to_bytes(4) + raw_items + PaddingUtils.impose_chunck_padding(raw_items)
    
    # ssrc or csrc
    # synchronised source or contribution source
    source : int
    
    # List of SDES items
    sdes_items : list[RTCPGenericItem]