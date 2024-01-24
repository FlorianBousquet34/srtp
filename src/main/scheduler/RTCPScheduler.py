
import datetime
from main.executor.RTCPJobExecutor import RTCPJobExecutor
from main.model.rtcp.RTCPParticipantState import RTCPParticipantState
from main.scheduler.RTCPTrsIntervalComputation import RTCPTransmissionIntervalComputation
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class RTCPScheduler:
    
    @staticmethod
    def scheduleNextRTCPMessage(state: RTCPParticipantState):

        # Scedule a job at tn to send a rtcp packet
        state.refresh()
        timeInterval = RTCPTransmissionIntervalComputation.computeRTCPTransmissionInterval(state)
        state.tn = timeInterval + (datetime.datetime.utcnow() - state.participantJoinTime).total_seconds()
        jobScheduleTime = datetime.timedelta(seconds=timeInterval) + datetime.datetime.utcnow()
        if state.rtcpScheduler is None:
            state.rtcpScheduler = AsyncIOScheduler()
        
        if state.rtcpScheduler.state == 0:
            state.rtcpScheduler.start()
            
        state.rtcpScheduler.add_job(RTCPJobExecutor.executeRTCPJobs(state.session), "date", jobScheduleTime)