from main.model.rtcp.sdes.items.RTCPItemEnum import RTCPItemEnum


class RTCPGenericItem:
    
    # On 8 bits
    sdes_key : RTCPItemEnum
    
    # octet count on 8 bits
    length: int
    
    # value on a fixed number of octets
    sdes_value: str
    