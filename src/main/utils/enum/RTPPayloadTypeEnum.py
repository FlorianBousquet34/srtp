from enum import Enum

# from 0 - 32 to avoid conflicts with SRTP
class RTPPayloadTypeEnum(Enum):
    
    # Codes for RTCP (control packet) from 0 to 4
    
    # Sender report from participants that are active senders
    RTCP_SR=0
    
    # Receiver report for reception statistics from participants
    #  that are not active senders and in combination with SR for
    #  active senders reporting on more than 31 sources
    RTCP_RR=1
    
    # Source description items, including CNAME
    RTCP_SDES=2
    
    # Indicates end of participation
    RTCP_BYE=3
    
    # Application-specific functions
    RTCP_APP=4