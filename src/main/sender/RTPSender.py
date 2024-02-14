from src.main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from src.main.model.rtcp.RTCPHeader import RTCPHeader
from src.main.model.rtcp.sdes.items.RTCPItemEnum import RTCPItemEnum
from src.main.model.rtp.RTPPacket import RTPPacket
from src.main.model.rtp.RTPSession import RTPSession
from src.main.utils.transformer.CNAMETransformer import CNAMETransformer


class RTPSender:
    
    @staticmethod
    def send_bye_packet(packet: RTPPacket | RTCPCompoundPacket, session: RTPSession):
        
        RTPSender.send_packet(packet, session)
        session.quit_session()
        
        
    @staticmethod
    def send_packet(packet: RTPPacket | RTCPCompoundPacket, session: RTPSession):

        ssrc : int
        if isinstance(packet, RTPPacket):
            ssrc = packet.header.fixed_header.ssrc
        else:
            i = 0
            while i < len(packet.packets) and not isinstance(packet.packets[i].packet.header, RTCPHeader):
                i += 1
            if not isinstance(packet.packets[i].packet.header, RTCPHeader):
                raise ValueError("No target ssrc found in RTCP Compound packet")
            else:
                ssrc = packet.packets[i].packet.header.ssrc
            
        if ( session.sdes_info.get(ssrc, None) and 
                session.sdes_info[ssrc].get(RTCPItemEnum.CNAME.value, None) is not None ):
            
            host, port = CNAMETransformer.transform_cname(session.sdes_info[ssrc][RTCPItemEnum.CNAME.value])
            
            session.profile.sock.sendto(packet.raw_data, (host, port))
        
            # Add ourselves to senders and activate we_send flag
            if session.senders.get(ssrc, None) is None:
                session.senders[ssrc] = session.participant
        
            if not session.participant.participant_state.we_send:
                session.participant.participant_state.we_send = True
        
        else:
            raise NameError("RTP Packet could not be sent to ssrc ", ssrc, " because no CNAME value could be found")