from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPSession import RTPSession


class RTPSender:
    
    def sendPacket(packet: RTPPacket | RTCPCompoundPacket, session: RTPSession):
        
        # TODO Send packet
        
        # Add ourselves to senders and activate we_send flag
        if session.senders.get(packet.header.fixedHeader.ssrc, None) is None:
            session.senders[packet.header.fixedHeader.ssrc] = session.participant
        
        if not session.participant.participantState.weSend:
            session.participant.participantState.weSend = True
        
        pass