from main.model.rtcp.sdes.items.RTCPItemEnum import RTCPItemEnum


class RTCPGenericItem:
    
    def to_bytes(self) -> bytearray:
        
        return self.sdes_key.value.to_bytes() + self.length.to_bytes() + self.sdes_value.encode()
    
    # On 8 bits
    sdes_key : RTCPItemEnum
    
    # octet count on 8 bits
    length: int
    
    # value on a fixed number of octets
    sdes_value: str
    