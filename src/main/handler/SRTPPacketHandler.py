from main.handler.RTPPacketHandler import RTPPacketHandler
from main.model.rtcp.RTCPPacket import RTCPPacket
from main.model.rtp.RTPPacket import RTPPacket
from main.model.srtcp.SRTCPPacket import SRTCPPacket
from main.model.srtp.SRTPPacket import SRTPPacket
from main.model.srtp.SRTPSession import SRTPSession


class SRTPPacketHandler:
    
    # TODO extra checks when handling srtcp compound packet (ie replay defence...)
    
    @staticmethod
    def handle_srtcp_packet(packet: SRTCPPacket, session: SRTPSession):
        
        RTPPacketHandler.handle_rtcp_packet(packet, session)
        
    @staticmethod
    def handle_non_srtcp_packet(packet: RTPPacket, session: SRTPSession):
        
        ssrc = packet.header.fixed_header.ssrc
        seq_num = packet.header.fixed_header.sequence_number
        
        session.increase_sequence_highest(seq_num, ssrc)
        session.add_seq_num_to_replay_list(seq_num, ssrc)
        
        RTPPacketHandler.handle_non_rtcp_packet(packet, session)