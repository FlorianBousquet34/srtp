import datetime
from main.model.rtp.RTPParticipant import RTPParticipant
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from main.model.rtp.RTPSessionContext import RTPProfile

DELETION_DELAY : float = 5.0

# After 5 RTCP Intervals without message from a
# source, it is recommanded to mark it inactive
RECEIVER_INACTIVITY_INTERVAL_COUNT : int = 5

SENDER_INACTIVITY_INTERVAL_COUNT : int = 2

class RTPSession:
    
    def __init__(self) -> None:
        self.latest_rtcp_timer = []
        self.leave_scheduler = AsyncIOScheduler()
        self.leave_scheduler.start()
    
    def participant_validation(self, ssrc) -> bool:
        validated : bool = True
        
        # TODO participant validation is based on SDES RTCP Packet
        # containing a CNAME received from the source or multiple
        # RTP Packet received from the same ssrc
        
        if validated :
            self.add_to_session(ssrc)
        else:
            if self.invalidated_members.get(ssrc, None) is None:
                self.invalidated_members[ssrc] = 1
            else:
                self.invalidated_members[ssrc] = self.invalidated_members[ssrc] + 1
        
        return validated
    
    def mark_bye_event(self, ssrc: int):
        
        # Mark a participant BYE Event and schedule him removal from session
        
        found = self.session_members.get(ssrc, None)
        if found:
            found.is_leaving = True
            scheduler : AsyncIOScheduler = self.leave_scheduler
            scheduler.add_job(self.remove_from_session(ssrc), 'date', datetime.datetime(second=DELETION_DELAY) 
                                + datetime.datetime.utcnow(), id=ssrc)
    
    def remove_from_session(self, ssrc: int):
        
        # Removes the participant with this ssrc from the session
        
        self.session_members.pop(ssrc, None)
        self.inactive_members.pop(ssrc, None)
        self.invalidated_members.pop(ssrc, None)
        self.inactive_tracker.pop(ssrc, None)
        self.senders.pop(ssrc, None)
    
    def add_to_session(self, ssrc : int, participant : RTPParticipant | None = None):
        
        # Add the ssrc to the session members
        if participant is None:
            self.session_members[ssrc] = RTPParticipant(ssrc)
        self.inactive_tracker[ssrc] = datetime.datetime.utcnow()
        self.session_members[ssrc].is_validated = True
    
    def update_inactive_participants(self):
        
        # Check if we have to mark members inactive
        if len(self.latest_rtcp_timer) >= RECEIVER_INACTIVITY_INTERVAL_COUNT:
            for member in self.session_members:
                self.latest_rtcp_timer.sort()
                if self.inactive_tracker[member] < self.latest_rtcp_timer[0]:
                    self.set_inactive(member)
            
        # Check if we have to remove senders
        if len(self.latest_rtcp_timer) >= SENDER_INACTIVITY_INTERVAL_COUNT:
            for sender in self.senders:
                self.latest_rtcp_timer.sort(reverse=True)
                if self.inactive_tracker[sender] < self.latest_rtcp_timer[1]:
                    self.senders.pop(sender, None)
                
    def set_inactive(self, ssrc: int):
        
        # Set a member inaction or remove it if the member is
        # not validated
        if self.invalidated_members.get(ssrc, None) is None:
            self.inactive_members[ssrc] = self.session_members[ssrc]
        self.inactive_tracker.pop(ssrc)
        self.session_members.pop(ssrc)
    
    def refresh_latest_rtcp_timers(self):
        
        self.latest_rtcp_timer.append(datetime.datetime.utcnow())
        if len(self.latest_rtcp_timer) > RECEIVER_INACTIVITY_INTERVAL_COUNT:
            self.latest_rtcp_timer.sort()
            self.latest_rtcp_timer.remove(self.latest_rtcp_timer[0])
        
        
            
    def add_to_sender(self, ssrc: int):
        
        if self.senders.get(ssrc, None) is None:
            # add the ssrc to senders
            member = self.session_members.get(ssrc, None)
            if member is None:
                # The sender may be invalidated
                if self.invalidated_members.get(ssrc, None) is not None:
                    self.senders[ssrc] = self.invalidated_members[ssrc]
            else:
                self.senders[ssrc] = self.session_members[ssrc]
            
    # The RTPSession Profile
    profile: RTPProfile
    
    # The RTCP transmission interval
    # Is calculated and increases with the number of participants
    # to limit traffic
    # Should use randomization
    transmission_interval: float
    
    # Session Start Time
    session_start: datetime.datetime
    
    # Session members
    session_members: dict[int, RTPParticipant] = {}
    
    # Session senders
    session_senders : dict[int, RTPParticipant] = {}

    # The Estimated Average Packet Size in octects
    # This depends of the application purpose
    average_packet_size: float
    
    # Leave scheduler
    leave_scheduler : AsyncIOScheduler
    
    # Unvalidated packet received
    invalidated_members : dict[int, int] = {}
    
    # Last packet Tracker keeps the date of the last RTP Packet received
    # from a source and is used to determine inactive members ssrc:tp
    inactive_tracker : dict[int, datetime.datetime] = {}
    
    # List of the inactive members
    inactive_members : dict[int, RTPParticipant] = {}
    
    # Client participant
    participant: RTPParticipant
    
    # Last 5 RTCP Timers
    latest_rtcp_timer : list[datetime.datetime] = []
    
    # Senders in this session
    senders : dict[int, RTPParticipant] = {}