import datetime
from main.executor.RTCPJobExecutor import RTCPJobExecutor
from main.model.rtp.RTPSession import RTPSession
from apscheduler.schedulers.background import BackgroundScheduler

class RTCPReverseAlgorithm:
    
    @staticmethod
    def apply_rtcp_reverse_algorithm(session: RTPSession):
        
        # The value for tn is updated according to the following formula:
        # tn = tc + (members/pmembers) * (tn - tc)
        tc = session.participant.participant_state.get_tc()
        session.participant.participant_state.tn = tc + session.participant.participant_state.members / session.participant.participant_state.pmembers * (
            session.participant.participant_state.tn - tc)
        
        
        # The value for tp is updated according the following formula:
        # tp = tc - (members/pmembers) * (tc - tp).
        session.participant.participant_state.tp = tc - session.participant.participant_state.members / session.participant.participant_state.pmembers * (
            tc - session.participant.participant_state.tp)

        # The next RTCP packet is rescheduled for transmission at time tn,
        # which is now earlier.
        rtcp_scheduler : BackgroundScheduler = session.participant.participant_state.rtcp_scheduler
        
        if session.participant.participant_state.rtcp_job is not None:
            
            time_interval = session.participant.participant_state.tn - (
                datetime.datetime.utcnow() - session.participant.participant_state.participant_join_time).total_seconds()
            
            job_schedule_time = datetime.timedelta(seconds=time_interval) + datetime.datetime.now()
            
            rtcp_scheduler.remove_job(session.participant.participant_state.rtcp_job.id)
            rtcp_scheduler.add_job(RTCPJobExecutor.execute_rtcp_jobs, trigger='date', next_run_time=job_schedule_time, args=[session])

        # The value of pmembers is set equal to members.
        session.participant.participant_state.pmembers = session.participant.participant_state.members