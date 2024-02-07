from datetime import datetime
from typing import Any
from apscheduler.job import Job
from main.model.rtcp.RTCPConsts import SECOND_TO_TIMESTAMP_MULTIPLIER, SEQ_NUM_BITS, SEQ_NUM_SIZE, TIMESTAMP_SIZE, TIMESTAMPS_BITS
from main.scheduler.RTCPScheduler import RTCPScheduler
from main.model.rtp.RTPSession import RTPSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main.threading.UDPHandlingThread import UDPHandlingThread
from main.threading.UDPListenningThread import UDPListenningThread
import random

class RTCPParticipantState :
    
    # The state for a given participant
    # !!! The curent time is initiated at 0
    # when the participant joins the session
    
    def __init__(self, session: RTPSession, participant) -> None:
        self.session = session
        self.target_bandwidth = session.profile.session_bandwidth * session.profile.control_bandwith_fraction
        self.average_packet_size = session.profile.estimated_packet_size
        self.participant = participant
        self.latest_seq_num = random.SystemRandom().getrandbits(SEQ_NUM_BITS)
        self.timestamp_offset = random.SystemRandom().getrandbits(TIMESTAMPS_BITS)
        self.participant_join_time = datetime.utcnow()
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
    
    def get_next_random_seq_num(self):
        
        latest_seq_num = (self.latest_seq_num + 1)
        if latest_seq_num >= SEQ_NUM_SIZE:
            self.participant.roc += 1
            self.latest_seq_num = latest_seq_num % SEQ_NUM_SIZE
        else:
            self.latest_seq_num = latest_seq_num
        return self.latest_seq_num
    
    def get_rtp_timestamp(self) -> int:
        
        return int((datetime.utcnow() - self.session.participant.participant_state.participant_join_time).total_seconds() * SECOND_TO_TIMESTAMP_MULTIPLIER
                + self.timestamp_offset) % TIMESTAMP_SIZE
    
    # The participant
    participant: Any
    
    # The Time the participant joined the session
    participant_join_time : datetime
    
    # Timestamp offset
    timestamp_offset: int
    
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
    
    # Latest seq num used, incremented by one for each RTP Packet send
    # and initiation must be random
    latest_seq_num : int