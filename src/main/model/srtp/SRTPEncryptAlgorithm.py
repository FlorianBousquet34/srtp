from main.model.srtp.SRTPSession import SRTPSession


class SRTPEncryptAlgorithm:
    
    def encrypt(self, data: bytearray, session: SRTPSession) -> bytearray:
        
        # TODO Encrypt
        
        pass
    
    def decrypt(self, data: bytearray, session: SRTPSession) -> bytearray:
        
        # TODO Decrypt
        
        pass
    
    #     *  BLOCK_CIPHER-MODE indicates the block cipher used and its mode of
    #       operation
    block_cipher_mode: str
    
    #    *  n_b is the bit-size of the block for the block cipher
    block_cipher_size : int
    
    #    *  n_e is the bit-length of k_e
    session_key_size : int
    
    #    *  n_s is the bit-length of k_s
    session_salt_length: int
    
    #    *  SRTP_PREFIX_LENGTH is the octet length of the keystream prefix, a
    #       non-negative integer, specified by the message authentication code
    #       in use.
    srtp_prefix_length: int = 0