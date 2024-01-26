from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPSession import RTPSession


class RTPSender:
    
    @staticmethod
    def send_packet(packet: RTPPacket | RTCPCompoundPacket, session: RTPSession):
        
        # TODO Send packet
        if isinstance(packet, RTPPacket):
            ssrc = packet.header.fixed_header.ssrc
        else:
            ssrc = packet.packets[0].packet.header.ssrc
        # Add ourselves to senders and activate we_send flag
        if session.senders.get(ssrc, None) is None:
            session.senders[ssrc] = session.participant
        
        if not session.participant.participant_state.we_send:
            session.participant.participant_state.we_send = True