from datetime import datetime
from main.scheduler.RTCPScheduler import RTCPScheduler
from main.model.rtp.RTPParticipant import RTPParticipant
from main.model.rtp.RTPSession import RTPSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class RTCPParticipantState :
    
    # The state for a given participant
    # !!! The curent time is initiated at 0
    # when the participant joins the session
    
    def __init__(self, session: RTPSession, participant: RTPParticipant) -> None:
        self.session = session
        self.targetBandwidth = session.profile.sessionBandwidth * session.profile.controlBandwithFraction
        self.averagePacketSize = session.profile.estimatedPacketSize
        self.participant = participant
        self.participantJoinTime = datetime.utcnow()
        RTCPScheduler.scheduleNextRTCPMessage(self)
        
    def refresh(self):
        
        # Refresh the state : tc, sender, members,
        
        self.tc = (datetime.utcnow() - self.participantJoinTime).total_seconds()
        self.members = len(self.session.sessionMembers)
        self.senders = len(self.session.senders)
    
    # The participant
    participant: RTPParticipant
    
    # The Time the participant joined the session
    participantJoinTime : datetime
    
    # The RTP Session of the participant
    session: RTPSession
    
    # The time of the last transmitted rtcp packet
    tp : float = 0
    
    # The current time
    # The refresh method needs to be called before
    # accessing this value
    tc : float = 0
    
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
    
    # The RTCP Job shceduler
    rtcpScheduler: AsyncIOScheduler