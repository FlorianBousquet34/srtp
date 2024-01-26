from main.model.srtp.SRTPAuthMessage import SRTPAuthMessage


class SRTPPacket:
    
    # The authentified part of the SRTP Packet
    auth_mesage: SRTPAuthMessage
    
    # a variable length auth tag calculated according to the current rollover counter,
    # the authentication algorithm indicated in the cryptographic context,
    # and the session authentication key found in Step 4.  Append the authentication tag to the packet.
    # length % 8 btis = 0
    auth_tag: list[str] = []
    
    # SRTP MKI of variable length MKI % 8 bits = 0
    master_key_identifier: list[str] = []
    
    # Whether or not the message is authentified or not or not yet
    authentified: bool | None = None
      