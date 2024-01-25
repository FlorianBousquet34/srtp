from main.model.rtcp.sdes.RTCPSDESItem import RTCPSDESItem


class RTCPSDEChunk:
    
    # ssrc or csrc
    # synchronised source or contribution source
    source : int
    
    # List of SDES items
    sdesItems : list[RTCPSDESItem]