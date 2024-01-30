from main.model.srtp.SRTPAuthenticationAlgorithmIdentifierEnum import SRTPAuthenticationAlgorithmIdentifierEnum
import hmac
import hashlib
import base64

class SRTPAuthAlgorithm:
    
    def __init__(self, algorithm_identifier: str = SRTPAuthenticationAlgorithmIdentifierEnum.HMACSHA1.value,
                n_a: int = 160, n_tag: int = 32, str_prefix_length: int = 0) -> None:
        self.n_a = n_a
        self.n_tag = n_tag
        self.str_prefix_length = str_prefix_length
        self.algorithm_identifier = algorithm_identifier
        
    def authenticate_message(self, session_key: bytearray, auth_tag: str, message: bytearray) -> bool:
        
        if len(auth_tag) * 8 != self.n_tag:
            return False
        else:
            return self.generate_auth_tag(session_key, message) == auth_tag
    
    def generate_auth_tag(self, session_key: bytearray, message: bytearray) -> str:
        
        if self.algorithm_identifier == SRTPAuthenticationAlgorithmIdentifierEnum.HMACSHA1.value:
                hmac_64 = hmac.new(session_key, message, hashlib.sha1).digest()
                return base64.urlsafe_b64encode(hmac_64).decode()
        if self.algorithm_identifier == SRTPAuthenticationAlgorithmIdentifierEnum.NONE.value:
            return ""
        # !!! implement other auth algorithm here
        else:
            raise ValueError("Auth algorithm not implemented", self.algorithm_identifier)
    
    # n_a is the bit-length of the authentication key
    n_a : int
   
    # n_tag is the bit-length of the output authentication tag
    n_tag : int
   
    # SRTP_PREFIX_LENGTH is the octet length of the keystream prefix as
    #   defined above, a parameter of AUTH_ALG
    str_prefix_length : int
    
    # The identifier of the algorithm to use
    algorithm_identifier : str