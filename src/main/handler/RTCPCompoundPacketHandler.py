from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtp.RTPSession import RTPSession

PACKET_AVG_CONTRIBUTION = 1.0 / 16.0

class RTCPCompoundPacketHandler:
    
    @staticmethod
    def handle_rtcp_compound_packet(packet: RTCPCompoundPacket, session: RTPSession):
         
        # TODO Split RTCP Compound Packets
        
        # Updating avg rtcp packet size
        session.participant.participant_state.average_packet_size = PACKET_AVG_CONTRIBUTION * len(packet.raw_data) + (
                    (1.0 - PACKET_AVG_CONTRIBUTION) *  session.participant.participant_state.average_packet_size)