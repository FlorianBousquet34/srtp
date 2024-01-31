from main.handler.RTPPacketHandler import RTPPacketHandler
from main.handler.SRTPPacketHandler import SRTPPacketHandler
from main.model.rtp.RTPPacket import RTPPacket
from main.model.srtcp.SRTCPCompoundPacket import SRTCPCompoundPacket
from main.model.srtp.SRTPAuthMessage import SRTPAuthMessage
from main.model.srtp.SRTPPacket import SRTPPacket
from main.model.srtp.SRTPSession import SRTPSession
from main.parser.RTPParser import RTPParser
from main.parser.SRTCPParser import SRTCPParser
from main.reader.RTPListenner import PACKET_AVG_CONTRIBUTION
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum


class SRTPListenner:
    
    @staticmethod
    def read_incoming_srtp_packet(data: bytearray, session: SRTPSession):
        
        packet = SRTPPacket()
        packet.raw_message = data
        if packet.authenticate_incoming_message(session):
            # all the auth related data has been added lets decrypt the message
            packet.auth_message.decrypt_auth_message(session)
            SRTPListenner.parse_srtp_packet(packet.auth_message, session)
        else:
            # handle auth error signal
            SRTPListenner.signal_auth_error(packet, session)
            
    @staticmethod
    def signal_auth_error(packet : SRTPPacket, session: SRTPSession):
        
        # !!! Implement what to do with bad authentification packets to monitor
        # failed attemps to join session
        
        pass
    
    @staticmethod
    def parse_srtp_packet(auth_message: SRTPAuthMessage, session: SRTPSession):
        data = auth_message.plain_message
        if data is not None and len(data) >= 2 :
            
            # check that V=2
            if data[0] >> 6 & 0b11 == 2:
                
                # it is rtp
                if (data[1] >> 7) & 1 != 0 and data & 0b1111111 in RTPPayloadTypeEnum.__members__.values():
                    
                    # it is a rtcp compound packet
                    packet = SRTCPCompoundPacket(data)
                    SRTCPParser.parse_rtcp_compound_packet(packet)
                    
                    # Updating avg rtcp packet size
                    session.participant.participant_state.average_packet_size = PACKET_AVG_CONTRIBUTION * len(packet.raw_data) + (
                        (1.0 - PACKET_AVG_CONTRIBUTION) *  session.participant.participant_state.average_packet_size)
                    
                    for srtcp_packet in packet.packets:
                        
                        SRTPPacketHandler.handle_srtcp_packet(srtcp_packet, session)
                else:
                    
                    # it is not a rtcp compound packet
                    packet = RTPPacket(data)
                    RTPParser.parse_rtp_packet(packet)
                    SRTPPacketHandler.handle_non_srtcp_packet(packet, session)
                    
                auth_message.rtp_packet = packet
            else:
                
                # it is not rtp
                raise TypeError("SRTP Version Should be 2", data[0] // 64, " was received")
            
        else:
            # packet size is too small
            raise ValueError("The received packet has no data")