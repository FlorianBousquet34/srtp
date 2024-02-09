from main.model.rtcp.sdes.items.RTCPItemEnum import RTCPItemEnum


class RTCPGenericItem:
    
    def to_bytes(self) -> bytearray:
        
        value_bytes = self.sdes_value.encode()
        self.length = len(value_bytes)
        return self.sdes_key.value.to_bytes() + self.length.to_bytes() + value_bytes
    
    # On 8 bits
    sdes_key : RTCPItemEnum
    
    # octet count on 8 bits
    length: int
    
    # value on a fixed number of octets
    sdes_value: str
    