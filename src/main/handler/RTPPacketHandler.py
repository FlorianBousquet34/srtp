
from datetime import datetime
from src.main.handler.RTCPReverseAlgorithm import RTCPReverseAlgorithm
from src.main.model.rtcp.RTCPPacket import RTCPPacket
from src.main.model.rtcp.rr.RTCPRRPacket import RTCPRRPacket
from src.main.model.rtcp.sdes.RTCPSDESPacket import RTCPSDESPacket
from src.main.model.rtcp.sr.RTCPSRPacket import RTCPSRPacket
from src.main.model.rtp.RTPHeader import RTPHeader
from src.main.model.rtp.RTPPacket import RTPPacket
from src.main.model.rtp.RTPSession import RTPSession
from src.main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum

class RTPPacketHandler:
    
    @staticmethod
    def handle_rtcp_packet(packet : RTCPPacket, session: RTPSession):

        if isinstance(packet.packet.header, RTPHeader) :
            
            # Handle inactivity exit
            RTPPacketHandler.handle_inactivity(packet.packet.header.ssrc, session)
        
        # All rtcp packets have this flag
        if packet.packet.header.marker:
        
            if packet.packet.header.payload_type == RTPPayloadTypeEnum.RTCP_BYE.value :
            
                RTPPacketHandler.handle_rtcp_bye_packet(packet, session)
            
            else:
                # Handle non BYE events
                if isinstance(packet.packet.header, RTPHeader) :
                    
                    # session participants handling
                    RTPPacketHandler.try_adding_participants_to_session(packet.packet.header.ssrc, session)
            
                
                # Treat according to message type
                if packet.packet.header.payload_type == RTPPayloadTypeEnum.RTCP_SR.value:
                    
                    RTPPacketHandler.handle_rtcp_sr_packet(packet.packet, session)
                
                elif packet.packet.header.payload_type == RTPPayloadTypeEnum.RTCP_RR.value:
                    
                    RTPPacketHandler.handle_rtcp_rr_packet(packet.packet, session)
                
                elif packet.packet.header.payload_type == RTPPayloadTypeEnum.RTCP_SDES.value :
                    
                    RTPPacketHandler.handle_rtcp_sdes_packet(packet.packet, session)
                
                elif packet.packet.header.payload_type == RTPPayloadTypeEnum.RTCP_APP.value :
                    
                    RTPPacketHandler.handle_rtcp_app_packet(packet.packet, session)                

                
    @staticmethod
    def handle_inactivity(ssrc : int, session : RTPSession):

        session.inactive_tracker[ssrc] = datetime.utcnow()
        if session.inactive_members.get(ssrc, None) is not None :
            session.inactive_members.pop(ssrc)
            session.add_to_session(ssrc)
                
    @staticmethod  
    def handle_non_rtcp_packet(packet : RTPPacket, session: RTPSession):
        
        ssrc = packet.header.fixed_header.ssrc
        
        session.add_to_latest_received(ssrc, packet)
                
        # session participants handling
        RTPPacketHandler.try_adding_participants_to_session(ssrc, session)
    
        # Handle inactivity exit
        RTPPacketHandler.handle_inactivity(ssrc, session)
        
        session.add_to_sender(ssrc)
        
        session.update_interarrival_jitter(ssrc, session.get_ntp_timestamp(), packet.header.fixed_header.timestamp)

        RTPPacketHandler.execute_packet_treatment(packet, session)

    @staticmethod
    def execute_packet_treatment(packet : RTPPacket, session: RTPSession):

        # !!! Override this method do do applicative packet treatment

        pass
        
            
            
    @staticmethod
    def handle_rtcp_bye_packet(packet : RTCPPacket, session: RTPSession):
        
        # Handle a BYE Packet received from another user
        # Remove the user from session members table
        
        for ssrc in packet.packet.sources:
            session.mark_bye_event(ssrc)
         
        RTCPReverseAlgorithm.apply_rtcp_reverse_algorithm(session)
         
          
         
    @staticmethod
    def handle_rtcp_sr_packet(packet : RTCPSRPacket, session: RTPSession):
        
        # handle a RTCP Sender Report packet
        session.update_last_sr_report(packet.sender_info.ntp_timestamp, packet.header.ssrc)
    
    @staticmethod
    def handle_rtcp_rr_packet(packet : RTCPRRPacket, session: RTPSession):
        
        # handle a RTCP Receiver Report packet
        pass
    
    @staticmethod
    def handle_rtcp_sdes_packet(packet : RTCPSDESPacket, session: RTPSession):
        
        # handle a RTCP SDES packet
        for chunck in packet.chuncks:
            
            ssrc = chunck.source
            if session.sdes_info.get(ssrc, None) is None:
                session.sdes_info[ssrc] = {}
                
            for sdes in chunck.sdes_items:
                session.sdes_info[ssrc][sdes.sdes_key] = sdes.sdes_value
    
    @staticmethod
    def handle_rtcp_app_packet(packet : RTCPPacket, session: RTPSession):
        
        # !!! Override this method to handle a RTCP APP packet
        
        pass
    
    @staticmethod
    def try_adding_participants_to_session(ssrc: int, session: RTPSession, csrc_list : list[int] | None = None):
        
        # Add ssrc and csrc to session members
        
        if session.session_members.get(ssrc, None) is None:
                # Validation of the new participant
                validated = session.participant_validation(ssrc)
                if validated and csrc_list is not None:
                    # If Validated we add the csrc
                    for csrc in csrc_list :
                        if session.session_members.get(csrc, None) is None:
                            session.participant_validation(csrc)