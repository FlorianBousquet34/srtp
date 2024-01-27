from main.utils.transformer.PaddingUtils import PaddingUtils


class RTPHeaderExtension:
    
    def to_bytes(self) -> bytearray:
        
        _ , text_padded, _ = PaddingUtils.pad_string(self.text)
        
        return self.extension_implem_identifier.to_bytes() + (len(text_padded) // 4 - 1).to_bytes()  + text_padded
    
    # a 16 bits identifier giving the signification of the extension
    extension_implem_identifier: int
    
    # The length of the extention payload on 16 bits
    # (length of wordlist)
    length: int 
    
    # list of size length of 32 bits words
    text: str