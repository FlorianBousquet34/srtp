from main.model.rtcp.sdes.items.RTCPGenericItem import RTCPGenericItem


class RTCPSDEChunk:
    
    # ssrc or csrc
    # synchronised source or contribution source
    source : int
    
    # List of SDES items
    sdes_items : list[RTCPGenericItem]