
from main.scheduler.RTCPScheduler import RTCPScheduler
from main.model.rtp.RTPParticipant import RTPParticipant


class RTCPJobExecutor:
    
    @staticmethod
    def executeRTCPJobs(participant : RTPParticipant):
        
        # TODO
        # Do the computation and send an RTCP Control packet
        # to all participants of the session
        
        RTCPScheduler.scheduleNextRTCPMessage(participant.participantState)