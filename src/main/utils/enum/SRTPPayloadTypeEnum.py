from enum import Enum

# from 32 to 63 to avoid conflicts with RTP
class SRTPPayloadTypeEnum(Enum):
    
    # Code for a heartbeat SRTCP message
    STCP=32