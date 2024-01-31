from main.handler.RTPPacketHandler import RTPPacketHandler
from main.model.srtcp.SRTCPPacket import SRTCPPacket
from main.model.srtp.SRTPPacket import SRTPPacket
from main.model.srtp.SRTPSession import SRTPSession


class SRTPPacketHandler:
    
    @staticmethod
    def handle_srtcp_packet(packet: SRTCPPacket, session: SRTPSession):
        
        # TODO extra checks when handling srtcp compound packet
        
        RTPPacketHandler.handle_rtcp_packet(packet, session)
        
    @staticmethod
    def handle_non_srtcp_packet(packet: SRTPPacket, session: SRTPSession):
        
        ssrc = packet.auth_message.rtp_packet.header.fixed_header.ssrc
        seq_num = packet.auth_message.rtp_packet.header.fixed_header.sequence_number
        
        session.increase_sequence_highest(seq_num, ssrc)
        session.add_seq_num_to_replay_list(seq_num, ssrc)
        
        RTPPacketHandler.handle_non_rtcp_packet(packet, session)