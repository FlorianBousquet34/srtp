
import datetime
from src.main.executor.RTCPJobExecutor import RTCPJobExecutor
from src.main.scheduler.RTCPTrsIntervalComputation import RTCPTrsIntervalComputation
from apscheduler.schedulers.background import BackgroundScheduler

class RTCPScheduler:
    
    @staticmethod
    def schedule_next_rtcp_message(state):
        
        # Scedule a job at tn to send a rtcp packet
        state.refresh()
        time_interval = RTCPTrsIntervalComputation.compute_rtcp_transmission_interval(state)
        state.tn = time_interval + (datetime.datetime.utcnow() - state.participant_join_time).total_seconds()
        job_schedule_time = datetime.timedelta(seconds=time_interval) + datetime.datetime.now()
        
        scheduler : BackgroundScheduler = state.rtcp_scheduler
        
        state.rtcp_job = scheduler.add_job(RTCPJobExecutor.execute_rtcp_jobs, trigger="date", next_run_time=job_schedule_time, args=[state.session])