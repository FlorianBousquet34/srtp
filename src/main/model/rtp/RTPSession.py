import datetime
from main.model.rtp.RTPParticipant import RTPParticipant
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from main.model.rtp.RTPSessionContext import RTPProfile

DELETION_DELAY : float = 5.0

# After 5 RTCP Intervals without message from a
# source, it is recommanded to mark it inactive
INACTIVITY_INTERVAL_COUNT : int = 5

class RTPSession:
    
    def __init__(self) -> None:
        self.latestRTCPTimer = []
        self.leaveScheduler = AsyncIOScheduler()
        self.leaveScheduler.start()
    
    def participantValidation(self, ssrc) -> bool:
        validated = True
        
        # TODO participant validation is based on SDES RTCP Packet
        # containing a CNAME received from the source or multiple
        # RTP Packet received from the same ssrc
        
        if validated :
            self.addToSession(ssrc)
        else:
            if self.invalidatedMembers.get(ssrc, None) is None:
                self.invalidatedMembers[ssrc] = 1
            else:
                self.invalidatedMembers[ssrc] = self.invalidatedMembers[ssrc] + 1
        
        return validated
    
    def markBYEEvent(self, ssrc: int):
        
        # Mark a participant BYE Event and schedule him removal from session
        
        found = self.sessionMembers.get(ssrc, None)
        if found:
            found.isLeaving = True
            scheduler : AsyncIOScheduler = self.leaveScheduler
            scheduler.add_job(self.removeFromSession(ssrc), 'date', datetime.datetime(second=DELETION_DELAY) + datetime.datetime.utcnow(), id=ssrc)
    
    def removeFromSession(self, ssrc: int):
        
        # Removes the participant with this ssrc from the session
        
        self.sessionMembers.pop(ssrc, None)
        self.inactiveMembers.pop(ssrc, None)
        self.invalidatedMembers.pop(ssrc, None)
        self.inactiveTracker.pop(ssrc, None)
        self.senders.pop(ssrc, None)
    
    def addToSession(self, ssrc : int):
        
        # Add the ssrc to the session members
        self.sessionMembers[ssrc] = RTPParticipant(ssrc)
        self.inactiveTracker[ssrc] = datetime.datetime.utcnow()
        self.sessionMembers[ssrc].isValidated = True
    
    def updateInactiveParticipants(self):
        
        # Check if we have to mark members inactive
        for member in self.sessionMembers:
            if self.inactiveTracker[member] < self.latestRTCPTimer.sort()[0]:
                self.setInactive(member)
                
    def setInactive(self, ssrc: int):
        
        # Set a member inaction or remove it if the member is
        # not validated
        if self.invalidatedMembers.get(ssrc, None) is None:
            self.inactiveMembers[ssrc] = self.sessionMembers[ssrc]
        self.inactiveTracker.pop(ssrc)
        self.sessionMembers.pop(ssrc)
        pass
    
    def refreshLatestRTCPTimers(self):
        
        self.latestRTCPTimer.append(datetime.datetime.utcnow())
        if len(self.latestRTCPTimer) > INACTIVITY_INTERVAL_COUNT:
            oldestTimer = self.latestRTCPTimer.sort()[0]
            self.latestRTCPTimer.remove(oldestTimer)
            
    def addToSender(self, ssrc: int):
        
        if self.senders.get(ssrc, None) is None:
            # add the ssrc to senders
            member = self.sessionMembers.get(ssrc, None)
            if member is None:
                # The sender may be invalidated
                if self.invalidatedMembers.get(ssrc, None) is not None:
                    self.senders[ssrc] = self.invalidatedMembers[ssrc]
            else:
                self.senders[ssrc] = self.sessionMembers[ssrc]
            
    # The RTPSession Profile
    profile: RTPProfile
    
    # The RTCP transmission interval
    # Is calculated and increases with the number of participants
    # to limit traffic
    # Should use randomization
    transmissionInterval: float
    
    # Session Start Time
    sessionStart: datetime.datetime
    
    # Session members
    sessionMembers: dict[int, RTPParticipant] = {}
    
    # Session senders
    sessionSenders : dict[int, RTPParticipant] = {}

    # The Estimated Average Packet Size in octects
    # This depends of the application purpose
    averagePacketSize: float
    
    # Leave scheduler
    leaveScheduler : AsyncIOScheduler
    
    # Unvalidated packet received
    invalidatedMembers : dict[int, int] = {}
    
    # Last packet Tracker keeps the date of the last RTP Packet received
    # from a source and is used to determine inactive members ssrc:tp
    inactiveTracker : dict[int, datetime.datetime] = {}
    
    # List of the inactive members
    inactiveMembers : dict[int, RTPParticipant] = {}
    
    # Client participant
    participant: RTPParticipant
    
    # Last 5 RTCP Timers
    latestRTCPTimer : list[datetime.datetime] = {}
    
    # Senders in this session
    senders : dict[int, RTPParticipant] = {}