from datetime import datetime
from main.scheduler.RTCPScheduler import RTCPScheduler
from main.model.rtp.RTPParticipant import RTPParticipant
from main.model.rtp.RTPSession import RTPSession


class RTCPParticipantState :
    
    # The state for a given participant
    # !!! The curent time is initiated at 0
    # when the participant joins the session
    
    def __init__(self, rtpSession: RTPSession, participant: RTPParticipant) -> None:
        self.rtpSession = rtpSession
        self.targetBandwidth = rtpSession.sessionBandwidth * rtpSession.controlBandwithFraction
        self.averagePacketSize = rtpSession.averagePacketSize
        self.participant = participant
        self.participantJoinTime = datetime.utcnow()
        RTCPScheduler.scheduleNextRTCPMessage(self)
    
    # The participant
    participant: RTPParticipant
    
    # The Time the participant joined the session
    participantJoinTime : datetime
    
    # The RTP Session of the participant
    rtpSession: RTPSession
    
    # The time of the last transmitted packet
    tp : float = 0
    
    # The time to send the next rtcp message
    tn : float
    
    # The number of members in session at last message
    pmembers: int = 1
    
    # The current number of members in session
    members: int = 1
    
    # The current number of senders in session
    senders: int = 0
    
    # The targeted bandwidth in octet per seconds
    # Should be smaller the the intended bandwith of
    # the session defined at session start
    targetBandwidth: float
    
    # The application has send a rtcp packet between
    # now and the 2nd last rtcp packet
    weSend: bool = False
    
    # The average size of packets received by this participant
    # in octets
    averagePacketSize: float
    
    # The particpant has not send packets yet
    initial: bool = True