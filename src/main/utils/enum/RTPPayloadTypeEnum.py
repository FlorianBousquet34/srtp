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
    # 202
    RTCP_SDES=74
    
    # Indicates end of participation
    # 203
    RTCP_BYE=75
    
    # Application-specific functions
    # 204
    RTCP_APP=76