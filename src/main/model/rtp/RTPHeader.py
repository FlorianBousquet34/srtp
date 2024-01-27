from main.model.rtp.RTPFixedHeader import RTPFixedHeader
from main.model.rtp.RTPHeaderExtension import RTPHeaderExtension


class RTPHeader:
    
    def to_bytes(self) -> bytearray:
        
        csrc_data = bytearray(len(self.csrc_list) * 4)
        
        for csrc_index in self.csrc_list:
            
            csrc_data[csrc_index * 4: ( csrc_index + 1 ) * 4] = self.csrc_list[csrc_index]
            
        extension_data = bytearray()
        if self.header_extension is not None :
            extension_data = self.header_extension.to_bytes()
        
        return self.fixed_header.to_bytes() + extension_data + csrc_data
    
    # The fixed length part of the header
    fixed_header: RTPFixedHeader
    
    # Enable the header extension implementations
    header_extension: RTPHeaderExtension | None
    
    # The list of constribution source (CSRC)
    # from 0 up to 15 items of 32 bits identifier
    csrc_list: list[int] = []
