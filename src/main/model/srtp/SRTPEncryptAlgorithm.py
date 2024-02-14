from src.main.model.rtcp.RTCPConsts import PACKET_INDEX_COEFFICIENT, SALT_COEFFICIENT, SSRC_COEFFICIENT
from src.main.model.srtp.SRTPEncryptionAlgorithmIdentifierEnum import SRTPEncryptionAlgorithmIdentifierEnum
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class SRTPEncryptAlgorithm:
    
    def __init__(self, session_key_size: int, session_salt_length: int,
                block_cipher_mode : str = "", srtp_prefix_length : int = 0, block_cipher_size: int = 16,
                algorithm_identifier: str = SRTPEncryptionAlgorithmIdentifierEnum.AES_COUNTER_MODE.value) -> None:
        self.block_cipher_mode = block_cipher_mode
        self.block_cipher_size = block_cipher_size
        self.session_key_size = session_key_size
        self.session_salt_length = session_salt_length
        self.srtp_prefix_length = srtp_prefix_length
        self.algorithm_identifier = algorithm_identifier
    
    def encrypt(self, data: bytearray, session, packet_index: int) -> bytearray:
        if self.algorithm_identifier == SRTPEncryptionAlgorithmIdentifierEnum.AES_COUNTER_MODE.value:
            iv = int((int.from_bytes(session.session_salting_key) * SALT_COEFFICIENT) ^ (session.participant.ssrc * SSRC_COEFFICIENT) ^ (packet_index * PACKET_INDEX_COEFFICIENT)).to_bytes(16)
            cipher = Cipher(algorithms.AES(session.session_encrypt_key), modes.CTR(iv))
            encryptor = cipher.encryptor()
            ct = encryptor.update(data) + encryptor.finalize()
            return ct
        # Implement other encryptions algorithm
        else:
            raise ValueError("Encryption algorithm not implemented ", self.algorithm_identifier)
            
            
    
    def decrypt(self, data: bytearray, session, packet_index: int) -> bytearray:
        if self.algorithm_identifier == SRTPEncryptionAlgorithmIdentifierEnum.AES_COUNTER_MODE.value:
            iv = int((int.from_bytes(session.session_salting_key) * SALT_COEFFICIENT) ^ (session.participant.ssrc * SSRC_COEFFICIENT) ^ (packet_index * PACKET_INDEX_COEFFICIENT)).to_bytes(16)
            cipher = Cipher(algorithms.AES(session.session_encrypt_key), modes.CTR(iv))
            decryptor = cipher.decryptor()
            plain = decryptor.update(data) + decryptor.finalize()
            return plain
        # Implement other encryptions algorithm
        else:
            raise ValueError("Encryption algorithm not implemented ", self.algorithm_identifier)
    
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
    srtp_prefix_length: int
    
    # Algorithm identifier
    # Possible values in SRTPEncryptionAlgorithmIdentifierEnum
    algorithm_identifier : str