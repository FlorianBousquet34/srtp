
from datetime import datetime
from main.handler.RTCPReverseAlgorithm import RTCPReverseAlgorithm
from main.model.rtcp.RTCPPacket import RTCPPacket
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPSession import RTPSession
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum


class RTCPPacketHandler:
    
    @staticmethod
    def handleRTCPPacket(packet : RTCPPacket, session: RTPSession):
        
        # TODO Maj
        
        # Handle inactivity exit
        RTCPPacketHandler.handleInactivity(packet.header.fixedHeader.ssrc, session)
        
        # All rtcp packets have this flag
        if packet.header.fixedHeader.marker:
        
            if packet.header.fixedHeader.payloadType == RTPPayloadTypeEnum.RTCP_BYE.value :
            
                RTCPPacketHandler.handleRTCPBYEPacket(packet, session)
            
            else:
                # Handle non BYE events
            
                # session participants handling
                RTCPPacketHandler.tryAddingParticipantsToSession(packet, session)
            
           
                
                # Treat according to message type
                if packet.header.fixedHeader.payloadType == RTPPayloadTypeEnum.RTCP_SR.value:
                    
                    RTCPPacketHandler.handleRTCPSRPacket(packet, session)
                
                elif packet.header.fixedHeader.payloadType == RTPPayloadTypeEnum.RTCP_RR.value:
                    
                    RTCPPacketHandler.handleRTCPRRPacket(packet, session)
                
                elif packet.header.fixedHeader.payloadType == RTPPayloadTypeEnum.RTCP_SDES.value :
                    
                    RTCPPacketHandler.handleRTCPSDESPacket(packet, session)
                
                elif packet.header.fixedHeader.payloadType == RTPPayloadTypeEnum.RTCP_APP.value :
                    
                    RTCPPacketHandler.handleRTCPAPPPacket(packet, session)                

                
    @staticmethod
    def handleInactivity(ssrc : int, session : RTPSession):

        session.inactiveTracker[ssrc] = datetime.utcnow()
        if session.inactiveMembers(ssrc, None) is not None :
            session.inactiveMembers.pop(ssrc)
            session.addToSession(ssrc)
                
    @staticmethod  
    def handleNonRTCPPacket(packet : RTPPacket, session: RTPSession):
        
        # Override this method to treat applicative packets
        
        # Handle inactivity exit
        RTCPPacketHandler.handleInactivity(packet.header.fixedHeader.ssrc, session)
        ssrc = packet.header.fixedHeader.ssrc
        session.addToSender(ssrc)
        
            
            
    @staticmethod
    def handleRTCPBYEPacket(packet : RTPPacket, session: RTPSession):
        
         # Handle a BYE Packet received from another user
         # Remove the user from session members table
         
         session.markBYEEvent(packet.header.fixedHeader.ssrc)
         
         RTCPReverseAlgorithm.applyRTCPReverseAlgorithm(packet, session)
         
          
         
    @staticmethod
    def handleRTCPSRPacket(packet : RTPPacket, session: RTPSession):
        
        # TODO handleRTCPSRPacket
        # handle a RTCP Sender Report packet
        pass
    
    @staticmethod
    def handleRTCPRRPacket(packet : RTPPacket, session: RTPSession):
        
        # TODO handleRTCPRRPacket
        # handle a RTCP Receiver Report packet
        pass
    
    @staticmethod
    def handleRTCPSDESPacket(packet : RTPPacket, session: RTPSession):
        
        # TODO handleRTCPSDESPacket
        # handle a RTCP SDES packet
        pass
    
    @staticmethod
    def handleRTCPAPPPacket(packet : RTPPacket, session: RTPSession):
        
        # TODO handleRTCPAPPPacket
        # handle a RTCP APP packet
        pass
    
    @staticmethod
    def tryAddingParticipantsToSession(packet: RTPPacket, session: RTPSession):
        
        # Add ssrc and csrc to session members
        
        if session.sessionMembers.get(packet.header.fixedHeader.ssrc, None) is None:
                # Validation of the new participant
                validated = session.participantValidation(packet.header.fixedHeader.ssrc)
                if validated:
                    # If Validated we add the csrc
                    for csrc in packet.header.csrcList :
                        session.participantValidation(csrc)