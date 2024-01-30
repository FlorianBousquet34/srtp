from main.model.rtp.RTPSession import RTPSession
from main.model.srtp.SRTPCryptoContext import SRTPCryptoContext


class SRTPSession(RTPSession):
    
    # The Cryptographic context of the SRTP Session
    crypto_context: SRTPCryptoContext
    
    # The session key to authenticate messages
    session_auth_key: bytearray
    
    # The session encryption key
    session_encrypt_key: bytearray
    
    # The session encrypyion salt
    session_salting_key: bytearray
    
    # the session master key identifier
    mki : int