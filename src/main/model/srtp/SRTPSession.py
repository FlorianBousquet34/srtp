from main.model.rtp.RTPSession import RTPSession
from main.model.rtp.RTPSessionContext import RTPSessionContext
from main.model.srtp.SRTPCryptoContext import SRTPCryptoContext
from expiringdict import ExpiringDict

class SRTPSession(RTPSession):
    
    # TODO Re-keying after 2^(n/2) packets encrypted
    
    def __init__(self, profile: RTPSessionContext, crypto_context: SRTPCryptoContext) -> None:
        
        super().__init__(profile)
        
        self.crypto_context = crypto_context
    
    def increase_roc(self, ssrc: int, max_seq_num: int):
        
        super().increase_roc(ssrc)
        
        self.sequence_highest[ssrc] = max_seq_num
        
    def increase_sequence_highest(self, seq_num: int, ssrc: int):
        
        if seq_num > self.sequence_highest.get(ssrc, 0):
            self.sequence_highest[ssrc] = seq_num
    
    def add_seq_num_to_replay_list(self, seq_num: int, ssrc: int):
        
        if self.replay_list.get(ssrc, None) is None:
            self.replay_list[ssrc] = ExpiringDict(self.crypto_context.replay_length, self.crypto_context.replay_timeout)
        self.replay_list[ssrc][seq_num] = True
    
    # The Cryptographic context of the SRTP Session
    crypto_context: SRTPCryptoContext
    
    # The session key to authenticate messages
    session_auth_key: bytearray
    
    # The session encryption key
    session_encrypt_key: bytearray
    
    # The session encryption salt
    session_salting_key: bytearray
    
    # the session master key identifier
    mki : int
    
    # highest extended sequence number received by source
    # in this roll
    sequence_highest : dict[int, int] = {}
    
    # A replay protection list of latest seq num by source
    replay_list : dict[int, ExpiringDict] = {}