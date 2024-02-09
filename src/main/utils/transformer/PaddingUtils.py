class PaddingUtils:
    
    @staticmethod
    def pad_string(text: str, pad_octets_modulo : int = 4, encoding: str = 'utf-8') -> (bool, bytearray, int):
        
        if pad_octets_modulo > 255:
            raise ValueError("Padding count may exceed octet size with modulo ", pad_octets_modulo)
        
        text_payload = bytearray(text, encoding)
        raw_payload_length = len(text_payload)
        if raw_payload_length % pad_octets_modulo == 0:
            # no padding needed
            return False, text_payload, 0
        else:
            padding_length = pad_octets_modulo - raw_payload_length % pad_octets_modulo
            count_octets = padding_length.to_bytes()
            
            return True, text_payload + bytearray(padding_length - 1) + count_octets, padding_length
        
    @staticmethod
    def impose_chunck_padding(data: bytearray, padding_mod: int = 4, impose_octets: int = 1) -> bytearray:
        
        length = len(data) + impose_octets
        padding_bytes = bytearray(impose_octets)
        if length % padding_mod != 0:
            pad_length = padding_mod - length % padding_mod
            padding_bytes += bytearray(pad_length)
            
        return data + padding_bytes