
from datetime import datetime
from main.model.rtp.RTPSession import RTPSession
from main.scheduler.RTCPScheduler import RTCPScheduler


class RTCPJobExecutor:
    
    @staticmethod
    def executeRTCPJobs(session : RTPSession):
        
        # TODO executeRTCPJobs
        # Do the computation and send an RTCP Compound packet
        # to all participants of the session
        session.refreshLatestRTCPTimers()
        session.updateInactiveParticipants()
        RTCPScheduler.scheduleNextRTCPMessage(session.participant.participantState)
        session.participant.participantState.tp = (datetime.utcnow() - session.participant.participantState.participantJoinTime).total_seconds()
        session.participant.participantState.pmembers = len(session.sessionMembers)
        session.participant.participantState.initial = False