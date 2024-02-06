from main.model.rtcp.RTCPConsts import HEADER_SIZE
from main.model.rtp.RTPPacket import RTPPacket
from main.model.srtcp.SRTCPCompoundPacket import SRTCPCompoundPacket
from main.model.srtp.SRTPSession import SRTPSession


class SRTPAuthMessage:
    
    def to_bytes(self, session: SRTPSession) -> bytearray:
        
        self.plain_message = self.rtp_packet.to_bytes()
        # RTP and RTCP Compound packet both start with a full header 8 bytes
        encrypted_payload = session.crypto_context.encrypt_algorithm.encrypt(self.plain_message[HEADER_SIZE:], session)
        self.raw_encrypted_message = self.plain_message[:HEADER_SIZE] + encrypted_payload
        return self.raw_encrypted_message
    
    def decrypt_auth_message(self, session: SRTPSession) -> None:
        
        # TO FIX handle not fully encrypted srtcp packet with E flag
        # We decrypt starting from raw_encrypted_message
        if len(self.raw_encrypted_message) >= HEADER_SIZE:
            
            decrypted_payload = session.crypto_context.encrypt_algorithm.decrypt(self.raw_encrypted_message[HEADER_SIZE:], session)
            self.plain_message = self.raw_encrypted_message[:HEADER_SIZE] + decrypted_payload
            
        else:
            raise ValueError("SRTP Packet was too small to parse header")
        
    
    rtp_packet : (RTPPacket | SRTCPCompoundPacket)
    
    # The encrypted message
    raw_encrypted_message: bytearray
    
    # The unencrypted message equivivalent to RTP
    plain_message: bytearray
    
    