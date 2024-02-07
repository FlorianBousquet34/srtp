
import datetime
from main.executor.RTCPJobExecutor import RTCPJobExecutor
from main.scheduler.RTCPTrsIntervalComputation import RTCPTrsIntervalComputation
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class RTCPScheduler:
    
    @staticmethod
    def schedule_next_rtcp_message(state):
        
        # Scedule a job at tn to send a rtcp packet
        state.refresh()
        time_interval = RTCPTrsIntervalComputation.compute_rtcp_transmission_interval(state)
        state.tn = time_interval + (datetime.datetime.utcnow() - state.participant_join_time).total_seconds()
        job_schedule_time = datetime.timedelta(seconds=time_interval) + datetime.datetime.utcnow()
        if state.rtcp_scheduler is None:
            state.rtcp_scheduler = AsyncIOScheduler()
        
        if state.rtcp_scheduler.state == 0:
            state.rtcp_scheduler.start()
            
        state.rtcp_job = state.rtcp_scheduler.add_job(RTCPJobExecutor.execute_rtcp_jobs(state.session), "date", job_schedule_time)