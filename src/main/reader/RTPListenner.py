from main.handler.RTPPacketHandler import RTPPacketHandler
from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.RTCPPacket import RTCPPacket
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPSession import RTPSession
from main.parser.RTCPParser import RTCPParser
from main.parser.RTPParser import RTPParser
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum

PACKET_AVG_CONTRIBUTION = 1.0 / 16.0

class RTPListenner:
    
    @staticmethod
    def read_incoming_rtp_packet(data: bytearray, session: RTPSession):
        
        if data is not None and len(data) >= 2 :
            
            # check that V=2
            if int((data >> 1) & 0b11) == 2:
                
                # it is rtp
                if (data >> 9) & 1 != 0 and int((data >> 10) & 0b1111111) in RTPPayloadTypeEnum.__members__.values():
                    
                    # it is a rtcp compound packet
                    packet = RTCPCompoundPacket(data)
                    RTCPParser.parse_rtcp_compound_packet(packet)
                    
                    # Updating avg rtcp packet size
                    session.participant.participant_state.average_packet_size = PACKET_AVG_CONTRIBUTION * len(packet.raw_data) + (
                        (1.0 - PACKET_AVG_CONTRIBUTION) *  session.participant.participant_state.average_packet_size)
                    
                    for rtcp_packet in packet.packets:
                        
                        RTPPacketHandler.handle_rtcp_packet(rtcp_packet)
                else:
                    
                    # it is not a rtcp compouns packet
                    packet = RTPPacket(data)
                    RTPParser.parse_rtp_packet(packet)
                    RTPPacketHandler.handle_non_rtcp_packet(packet, session)
                    
            else:
                
                # it is not rtp
                raise TypeError("RTP Version Should be 2", data[0] / 64, " was received")
            
        else:
            # packet size is too small
            raise ValueError("The received packet has no data")