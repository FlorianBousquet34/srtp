import datetime
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPSession import RTPSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
        rtcp_scheduler : AsyncIOScheduler = session.participant.participant_state.rtcp_scheduler
        
        if session.participant.participant_state.rtcp_job is not None:
            
            time_interval = session.participant.participant_state.tn - (
                datetime.datetime.utcnow() - session.participant.participant_state.participant_join_time).total_seconds()
            
            job_schedule_time = datetime.timedelta(seconds=time_interval) + datetime.datetime.utcnow()
            
            rtcp_scheduler.reschedule_job(session.participant.participant_state.rtcp_job.id, 'date', job_schedule_time)

        # The value of pmembers is set equal to members.
        session.participant.participant_state.pmembers = session.participant.participant_state.members