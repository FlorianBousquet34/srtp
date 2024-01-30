from main.handler.RTPPacketHandler import RTPPacketHandler
from main.model.srtcp.SRTCPPacket import SRTCPPacket
from main.model.srtp.SRTPSession import SRTPSession


class SRTPPacketHandler:
    
    @staticmethod
    def handle_srtcp_packet(packet: SRTCPPacket):
        
        # TODO extra checks when handling srtcp compound packet
        
        RTPPacketHandler.handle_rtcp_packet(packet)
        
    @staticmethod
    def handle_non_srtcp_packet(packet: SRTCPPacket, session: SRTPSession):
        
        # TODO extra checks when handling srtp packet
        
        RTPPacketHandler.handle_non_rtcp_packet(packet, session)