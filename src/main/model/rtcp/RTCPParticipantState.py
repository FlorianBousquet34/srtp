from datetime import datetime
from apscheduler.job import Job
from main.scheduler.RTCPScheduler import RTCPScheduler
from main.model.rtp.RTPParticipant import RTPParticipant
from main.model.rtp.RTPSession import RTPSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main.threading.UDPHandlingThread import UDPHandlingThread

from main.threading.UDPListenningThread import UDPListenningThread

class RTCPParticipantState :
    
    # The state for a given participant
    # !!! The curent time is initiated at 0
    # when the participant joins the session
    
    def __init__(self, session: RTPSession, participant: RTPParticipant) -> None:
        self.session = session
        self.target_bandwidth = session.profile.session_bandwidth * session.profile.control_bandwith_fraction
        self.average_packet_size = session.profile.estimated_packet_size
        self.participant = participant
        self.participantjoin_time = datetime.utcnow()
        self.listenning_thread = UDPListenningThread(session)
        RTCPScheduler.schedule_next_rtcp_message(self)
        
    def refresh(self):
        
        # Refresh the state : tc, sender, members,
        
        self.tc = self.get_tc()
        self.members = len(self.session.session_members)
        self.senders = len(self.session.senders)
        
    def get_tc(self):
        
        # get the real time relative to participant joinning session
        return (datetime.utcnow() - self.participant_join_time).total_seconds()
    
    # The participant
    participant: RTPParticipant
    
    # The Time the participant joined the session
    participant_join_time : datetime
    
    # The RTP Session of the participant
    session: RTPSession
    
    # The time of the last transmitted rtcp packet
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
    target_bandwidth: float
    
    # The application has send a rtcp packet between
    # now and the 2nd last rtcp packet
    we_send: bool = False
    
    # The average size of packets received by this participant
    # in octets
    average_packet_size: float
    
    # The particpant has not send packets yet
    initial: bool = True
    
    # The RTCP Job shceduler
    rtcp_scheduler: AsyncIOScheduler
    
    # next BYE job (used to reschedule)
    bye_job : Job
    
    # next rtcp job (used to reschedule or cancel)
    rtcp_job : Job
    
    # A Listening thread
    listenning_thread: UDPListenningThread
    
    # Handling thread
    handling_thread: UDPHandlingThread