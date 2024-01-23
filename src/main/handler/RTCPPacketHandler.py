
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPParticipant import RTPParticipant
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum


class RTCPPacketHandler:
    
    @staticmethod
    def handleRTCPPacket(packet : RTPPacket, paticipant : RTPParticipant):
        
        if(packet.header.extensionImplemIdentifier == RTPPayloadTypeEnum.RTCP_BYE.value):
            
            RTCPPacketHandler.handleRTCPBYEPacket(packet)
            
        else:
            # Handle non BYE events
            # Check if the sender is in the session member, if not
            # add him to the session members
            if not (paticipant in paticipant.participantState.rtpSession.sessionMembers):
                
                # TODO
                # Add participant to session members table and treat according to message type
                pass
            
            
            
            
    @staticmethod
    def handleRTCPBYEPacket(packet : RTPPacket):
        
         # TODO
         # Handle a BYE Packet received from another user
         # Remove the user from session members table
         
         pass
            