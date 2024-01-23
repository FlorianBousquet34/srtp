
import math
import random
from main.model.rtcp.RTCPParticipantState import RTCPParticipantState


class RTCPTransmissionIntervalComputation:
    
    SENDER_PERCENT_INCREMENT_SPLITTER : float = 0.25
    SENDER_BANDWIDTH_COEFFICIENT: float = 0.25
    RECEIVER_BANDWIDTH_COEFFICIENT: float = 0.75
    T_MIN_INITIALIZED: float = 5
    T_MIN_NOT_INITIALIZED: float = 2.5
    COMPENSATION_FACTOR : float = math.e - 1.5
    
    @staticmethod
    def computeRTCPTransmissionInterval(state: RTCPParticipantState):
        
        # This procedure results in an interval which is random, but which, on
        # average, gives at least 25% of the RTCP bandwidth to senders and the
        # rest to receivers.  If the senders constitute more than one quarter
        # of the membership, this procedure splits the bandwidth equally among
        # all participants, on average.
        
        c = 0
        n = 0
        if(state.senders <= RTCPTransmissionIntervalComputation.SENDER_PERCENT_INCREMENT_SPLITTER * state.members):
            # The senders represent less than 25% of members
            if(state.weSend):
                # The participant is a sender
                c = state.averagePacketSize / (RTCPTransmissionIntervalComputation.SENDER_BANDWIDTH_COEFFICIENT * state.targetBandwidth)
                n = state.senders
            else:
                # The participant is not a sender
                c = state.averagePacketSize / (RTCPTransmissionIntervalComputation.RECEIVER_BANDWIDTH_COEFFICIENT * state.targetBandwidth)
                n = state.members - state.senders
        else:
            # The senders are more than 25% of members
            c = state.averagePacketSize / state.targetBandwidth
            n = state.members
        Tmin = RTCPTransmissionIntervalComputation.T_MIN_INITIALIZED
        if(state.initial):
            Tmin = RTCPTransmissionIntervalComputation.T_MIN_NOT_INITIALIZED
        # deterministic calculated interval
        td = max(Tmin, n * c)
        # calculated interval
        t = random.uniform(0.5, 1.5) * td
        return t / RTCPTransmissionIntervalComputation.COMPENSATION_FACTOR