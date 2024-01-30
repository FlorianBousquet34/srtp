from enum import Enum


class SRTPAuthenticationAlgorithmIdentifierEnum(Enum):
    
    # No authentification (Not recommanded)
    NONE="NONE"
    
    HMACSHA1="HMAC-SHA1"