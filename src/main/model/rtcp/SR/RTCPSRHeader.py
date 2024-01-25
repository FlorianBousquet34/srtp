from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum


class RTCPSRHeader:
    
    marker: bool = True
    payloadType: int = RTPPayloadTypeEnum.RTCP_SR.value
    # V on 2 bits
    version: str
    
    # P padding on 1 bit
    padding: bool = False
    
    # RC on 4 bits
    receptionReportCount: int 
    
    #The length of this RTCP packet in 32-bit words minus one,
    # including the header and any padding
    length: int

    # SSRC synchronized source on 32 bits
    ssrc: int 