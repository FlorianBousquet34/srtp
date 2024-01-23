from datetime import datetime
from main.model.rtp.RTPParticipant import RTPParticipant


class RTPSession:
    
    # The RTCP transmission interval
    # Is calculated and increases with the number of participants
    # to limit traffic
    # Should use randomization
    transmissionInterval: float
    
    # Session Start Time
    sessionStart: datetime
    
    # Session members
    sessionMembers: list[RTPParticipant]
    
    # Session total bandwith for all participants in octets per seconds
    sessionBandwidth: float
    
    # Fraction of bandwidth allocated to HeartBeat (RTCP / SRTCP)
    # Between 0 and 1
    controlBandwithFraction: float
    
    # The Estimated Average Packet Size in octects
    # This depends of the application purpose
    averagePacketSize: float