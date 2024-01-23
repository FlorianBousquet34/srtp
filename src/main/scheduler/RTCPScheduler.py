
import datetime
from main.model.rtcp.RTCPParticipantState import RTCPParticipantState
from main.scheduler.RTCPTrsIntervalComputation import RTCPTransmissionIntervalComputation

class RTCPScheduler:
    
    @staticmethod
    def scheduleNextRTCPMessage(state: RTCPParticipantState):

        # Scedule a job at tn to send a rtcp packet
        
        state.tn = RTCPTransmissionIntervalComputation.computeRTCPTransmissionInterval(state)
        jobScheduleTime = datetime.timedelta(seconds=state.tn) + state.participantJoinTime
        
        # TODO Signal a RTCP Thread to execute a RTCP job at this time
