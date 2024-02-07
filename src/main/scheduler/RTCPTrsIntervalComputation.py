
import math
import random

class RTCPTrsIntervalComputation:
    
    SENDER_PERCENT_INCREMENT_SPLITTER : float = 0.25
    SENDER_BANDWIDTH_COEFFICIENT: float = 0.25
    RECEIVER_BANDWIDTH_COEFFICIENT: float = 0.75
    T_MIN_INITIALIZED: float = 5
    T_MIN_NOT_INITIALIZED: float = 2.5
    COMPENSATION_FACTOR : float = math.e - 1.5
    
    @staticmethod
    def compute_rtcp_transmission_interval(state):
        
        # This procedure results in an interval which is random, but which, on
        # average, gives at least 25% of the RTCP bandwidth to senders and the
        # rest to receivers.  If the senders constitute more than one quarter
        # of the membership, this procedure splits the bandwidth equally among
        # all participants, on average.
        
        c = 0
        n = 0
        if(state.senders <= RTCPTrsIntervalComputation.SENDER_PERCENT_INCREMENT_SPLITTER * state.members):
            # The senders represent less than 25% of members
            if(state.we_send):
                # The participant is a sender
                c = state.average_packet_size / (RTCPTrsIntervalComputation.SENDER_BANDWIDTH_COEFFICIENT * state.target_bandwidth)
                n = state.senders
            else:
                # The participant is not a sender
                c = state.average_packet_size / (RTCPTrsIntervalComputation.RECEIVER_BANDWIDTH_COEFFICIENT * state.target_bandwidth)
                n = state.members - state.senders
        else:
            # The senders are more than 25% of members
            c = state.average_packet_size / state.target_bandwidth
            n = state.members
        t_min = RTCPTrsIntervalComputation.T_MIN_INITIALIZED
        if(state.initial):
            t_min = RTCPTrsIntervalComputation.T_MIN_NOT_INITIALIZED
        # deterministic calculated interval
        td = max(t_min, n * c)
        # calculated interval
        t = random.uniform(0.5, 1.5) * td
        return t / RTCPTrsIntervalComputation.COMPENSATION_FACTOR