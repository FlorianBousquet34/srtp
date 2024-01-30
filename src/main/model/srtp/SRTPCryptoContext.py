from main.model.rtp.RTPSessionContext import RTPSessionContext


class SRTPCryptoContext(RTPSessionContext):
    
    # The authentication algorithm (can be NONE but not recommanded)
    # Can be probided by the SRTPAuthenticationAlgorithmIdentifierEnum
    auth_algorithm: str