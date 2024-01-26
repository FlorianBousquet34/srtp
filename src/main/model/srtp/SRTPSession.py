from main.model.rtp.RTPSession import RTPSession
from main.model.srtp.SRTPCryptoContext import SRTPCryptoContext


class SRTPSession(RTPSession):
    
    # The Cryptographic context of the SRTP Session
    crypto_context: SRTPCryptoContext