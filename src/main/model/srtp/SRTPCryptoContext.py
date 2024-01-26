from main.model.rtp.RTPSessionContext import RTPProfile


class SRTPCryptoContext(RTPProfile):
    
    # The authentication algorithm (can be NONE but not recommanded)
    # Can be probided by the SRTPAuthenticationAlgorithmIdentifierEnum
    auth_algorithm: str