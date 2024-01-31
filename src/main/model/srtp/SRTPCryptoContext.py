from main.model.rtp.RTPSessionContext import RTPSessionContext
from main.model.srtp.SRTPAuthAlgorithm import SRTPAuthAlgorithm
from main.model.srtp.SRTPEncryptAlgorithm import SRTPEncryptAlgorithm


class SRTPCryptoContext(RTPSessionContext):
    
    # The authentication algorithm (can be NONE but not recommanded)
    auth_algorithm: SRTPAuthAlgorithm
    
    # The encrypt algorithm used for the session
    encrypt_algorithm : SRTPEncryptAlgorithm
    
    # Whether or not the session MKI should be passed in the SRTP Packet
    pass_mki: bool = False
    
    # The length of the session mki in octets
    mki_length : int = 4
    
    # replay list length
    replay_length : int = 20
    
    # replay list timeout in seconds
    replay_timeout : int = 30