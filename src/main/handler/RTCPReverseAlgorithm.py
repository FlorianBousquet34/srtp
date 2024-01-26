from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPSession import RTPSession


class RTCPReverseAlgorithm:
    
    @staticmethod
    def apply_rtcp_reverse_algorithm(packet: RTPPacket, session: RTPSession):
        
        # TODO reverse reconsideration algorithm
        
        # The value for tn is updated according to the following formula:
        # tn = tc + (members/pmembers) * (tn - tc)
        
        # The value for tp is updated according the following formula:
        # tp = tc - (members/pmembers) * (tc - tp).

        # The next RTCP packet is rescheduled for transmission at time tn,
        # which is now earlier.

        # The value of pmembers is set equal to members.
        
        # !!! State must be updated
        
        pass