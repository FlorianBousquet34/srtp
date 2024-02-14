from src.main.model.srtp.SRTPAuthMessage import SRTPAuthMessage
from src.main.model.srtp.SRTPSession import SRTPSession


class SRTPPacket:
    
    def to_bytes(self, session: SRTPSession) -> bytearray:
        
        # transform the message model to data bytes
        self.auth_message.to_bytes(session)
        # create the auth tag
        self.authenticate_outgoing_message(session)
        
        # add the mki if needed in session context
        mki = bytearray()
        if session.crypto_context.pass_mki:
            mki = session.mki.to_bytes(session.crypto_context.mki_length)
        
        # get the full message data
        self.raw_message = self.auth_message.raw_encrypted_message + mki + self.auth_tag.encode()
        
        return self.raw_message
    
    def authenticate_incoming_message(self, session: SRTPSession) -> bool:
        
        # get the offsets due to authentication
        mki_offset = 0
        if session.crypto_context.pass_mki:
            mki_offset = session.crypto_context.mki_length
        
        auth_offset = session.crypto_context.auth_algorithm.n_tag // 8
        
        # get the auth tag provided in the message
        self.auth_tag = self.raw_message[-auth_offset:].decode()
        
        # get the authenticated message
        self.auth_message = SRTPAuthMessage()
        self.auth_message.raw_encrypted_message = self.raw_message[:-auth_offset -mki_offset]
        
        # play the auth algorith
        self.authenticated = session.crypto_context.auth_algorithm.authenticate_message(session.session_auth_key, self.auth_tag, self.auth_message.raw_encrypted_message)
        
        # save the mki given
        if self.authenticated and session.crypto_context.pass_mki:
            self.master_key_identifier = self.raw_message[-auth_offset-mki_offset:-auth_offset]
            
        return self.authenticated
    
    def authenticate_outgoing_message(self, session: SRTPSession):
        
        self.auth_tag = session.crypto_context.auth_algorithm.generate_auth_tag(session.session_auth_key, self.auth_message.raw_encrypted_message)
        self.authenticated = True
    
    # The authentified part of the SRTP Packet
    auth_message: SRTPAuthMessage
    
    # a variable length auth tag calculated according to the current rollover counter,
    # the authentication algorithm indicated in the cryptographic context,
    # and the session authentication key found in Step 4.  Append the authentication tag to the packet.
    # length % 8 btis = 0
    auth_tag: str
    
    # SRTP MKI of variable length MKI % 8 bits = 0
    master_key_identifier: bytearray
    
    # Whether or not the message is authenticated or not or not yet
    authenticated: bool | None = None
    
    raw_message: bytearray