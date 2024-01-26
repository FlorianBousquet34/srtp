
from datetime import datetime
from main.model.rtp.RTPSession import RTPSession
from main.scheduler.RTCPScheduler import RTCPScheduler


class RTCPJobExecutor:
    
    @staticmethod
    def execute_rtcp_jobs(session : RTPSession):
        
        # TODO executeRTCPJobs
        # Do the computation and send an RTCP Compound packet
        # to all participants of the session
        session.refresh_latest_rtcp_timers()
        session.update_inactive_participants()
        RTCPScheduler.schedule_next_rtcp_message(session.participant.participant_state)
        session.participant.participant_state.tp = (datetime.utcnow() - session.participant.participant_state.participant_join_time).total_seconds()
        session.participant.participant_state.pmembers = len(session.session_members)
        session.participant.participant_state.initial = False