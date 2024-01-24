from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtp.RTPSession import RTPSession

PACKET_AVG_CONTRIBUTION = 1.0 / 16.0

class RTCPCompoundPacketHandler:
    
    def handleRTCPCompoundPacket(packet: RTCPCompoundPacket, session: RTPSession):
         
        # TODO Split RTCP Compound Packets
        
        # Updating avg rtcp packet size
        session.participant.participantState.averagePacketSize = PACKET_AVG_CONTRIBUTION * len(packet.rawData) + (
                    (1.0 - PACKET_AVG_CONTRIBUTION) *  session.participant.participantState.averagePacketSize)