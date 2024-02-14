from src.main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from src.main.model.srtcp.SRTCPPacket import SRTCPPacket


class SRTCPCompoundPacket(RTCPCompoundPacket):

    packets : list[SRTCPPacket] = []
    