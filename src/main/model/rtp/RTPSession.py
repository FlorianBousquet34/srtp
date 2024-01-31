import datetime
from main.model.rtcp.sdes.items.RTCPGenericItem import RTCPGenericItem
from main.model.rtcp.sdes.items.RTCPItemEnum import RTCPItemEnum
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPParticipant import RTPParticipant
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from main.model.rtp.RTPSessionContext import RTPSessionContext

DELETION_DELAY : float = 5.0

# After 5 RTCP Intervals without message from a
# source, it is recommanded to mark it inactive
RECEIVER_INACTIVITY_INTERVAL_COUNT : int = 5

SENDER_INACTIVITY_INTERVAL_COUNT : int = 2

JITTER_MULTIPLIER : int = 16

NTP_TIMESTAMP_MULTIPLIER : int = int(1e6)

class RTPSession:
    
    def __init__(self, profile: RTPSessionContext) -> None:
        self.latest_rtcp_timer = []
        self.profile = profile
        self.leave_scheduler = AsyncIOScheduler()
        self.leave_scheduler.start()
    
    def participant_validation(self, ssrc) -> bool:
        
        # Participant validation is based on SDES RTCP Packet containing a CNAME
        # received from the source or multiple RTP Packet received from the same ssrc
        validated = ( self.sdes_info.get(ssrc, None) is not None and 
                        self.sdes_info[ssrc].get(RTCPItemEnum.CNAME.value, None) is not None )
        
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
    
    def add_to_latest_received(self, ssrc: int, packet: RTPPacket):
        
        if self.lastest_received.get(ssrc, None) is None:
            self.lastest_received[ssrc] = [packet]
        else:
            self.lastest_received[ssrc].append(packet)
            
    def update_last_sr_report(self, ntp_timestamp: int, source: int):
        
        ntp_bytes = ntp_timestamp.to_bytes(8)
        mid_ntp = int.from_bytes(ntp_bytes[2:6])
        self.latest_sr_report[source] = (mid_ntp, self.get_ntp_timestamp())
            
    def get_ntp_timestamp(self) -> int:
        
        return int((datetime.datetime.utcnow() - self.session_start).total_seconds() * NTP_TIMESTAMP_MULTIPLIER)
    
    def update_interarrival_jitter(self, source: int, arrival_time: int, sent_time: int):
        
        if self.last_difference.get(source, None) is None:
            self.last_difference[source] = arrival_time - sent_time
            self.interarrival_jitter[source] = 0
        else:
            difference = abs(self.last_difference[source] - (arrival_time - sent_time))
            self.interarrival_jitter[source] += (difference - self.interarrival_jitter[source]) / JITTER_MULTIPLIER
            self.last_difference[source] = arrival_time - sent_time
            
    def increase_roc(self, ssrc: int, _):
        
        if self.seq_num_roll.get(ssrc, None) is None:
            self.seq_num_roll[ssrc] = 1
        else:
            self.seq_num_roll[ssrc] += 1
            
    # The RTPSession Profile
    profile: RTPSessionContext
    
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
    
    # most recent sdes infos
    sdes_info : dict[int, dict[int, str]]
    
    # Waiting to leave is a flag activated when the user wants to
    # send a BYE packet but has to wait because there are more than
    # 50 participants in the session
    # !!! This flag modify the counting of members to counting BYE Packets
    # received
    # TODO implement this behaviour
    waiting_to_leave_50 : bool = False
    
    # Packets received since last RTCP
    lastest_received : dict[int, list[RTPPacket]] = {}
    
    # Packets sent since last RTCP
    latest_sent : list[RTPPacket] = []
    
    # Current seq num roll per source
    seq_num_roll : dict[int, int] = {}
    
    # Last SR ntp_timestamp midle 32-bits of source and
    # receiving ntp_timestamp of sr packet
    latest_sr_report: dict[int, (int, int)] = {}
    
    # The updated interrival jitter of each sources
    interarrival_jitter: dict[int, int] = {}
    
    # The last reception time difference D(i-1) = (Ri - Si)
    # used for interarrival jitter computation
    last_difference: dict[int, int] = {}