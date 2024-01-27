from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtcp.sdes.items.RTCPItemEnum import RTCPItemEnum
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPSession import RTPSession
from main.utils.transformer.CNAMETransformer import CNAMETransformer


class RTPSender:
    
    @staticmethod
    def send_packet(packet: RTPPacket | RTCPCompoundPacket, session: RTPSession):
        ssrc : int
        if isinstance(packet, RTPPacket):
            ssrc = packet.header.fixed_header.ssrc
        else:
            ssrc = packet.packets[0].packet.header.ssrc
            
        if ( session.sdes_info.get(ssrc, None) and 
                session.sdes_info[ssrc].get(RTCPItemEnum.CNAME.value, None) is not None ):
            
            host, port = CNAMETransformer.transform_cname(session.sdes_info[ssrc][RTCPItemEnum.CNAME.value])
            
            session.profile.sock.sendto(packet.raw_data, (host, port))
        
            # Add ourselves to senders and activate we_send flag
            if session.senders.get(ssrc, None) is None:
                session.senders[ssrc] = session.participant
        
            if not session.participant.participant_state.we_send:
                session.participant.participant_state.we_send = True