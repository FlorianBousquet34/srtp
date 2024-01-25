from enum import Enum

class RTPPayloadTypeEnum(Enum):
    
    # Codes for RTCP (control packet) from 0 to 4
    
    # Sender report from participants that are active senders
    #(200) => M=1 && PayloadType = 72
    RTCP_SR=72
    
    # Receiver report for reception statistics from participants
    #  that are not active senders and in combination with SR for
    #  active senders reporting on more than 31 sources
    # 201 => M=1 && PT = 73
    RTCP_RR=73
    
    # Source description items, including CNAME
    RTCP_SDES=74
    
    # Indicates end of participation
    RTCP_BYE=3
    
    # Application-specific functions
    RTCP_APP=4