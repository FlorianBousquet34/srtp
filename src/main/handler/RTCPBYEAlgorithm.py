from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.bye.RTCPBYEPacket import RTCPBYEPacket
from main.model.rtcp.bye.RTCPBYEReason import RTCPBYEReason
from main.model.rtp.RTPSession import RTPSession
from main.sender.RTPSender import RTPSender
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum

SESSION_MEMBERS_THRESHOLD : int = 50

class RTCPBYEAlgorithm:
    
    @staticmethod
    def execute_bye_algorithm(session: RTPSession):
        
        # TODO Transmitting a BYE Packet
        # https://datatracker.ietf.org/doc/html/rfc3550#section-6.3.7
        # if the number of members is more than 50 when the participant chooses to
        # leave.  This algorithm usurps the normal role of the members variable
        # to count BYE packets instead:

        # When the participant decides to leave the system, tp is reset to
        # tc, the current time, members and pmembers are initialized to 1,
        # initial is set to 1, we_sent is set to false, senders is set to 0,
        # and avg_rtcp_size is set to the size of the compound BYE packet.
        # The calculated interval T is computed.  The BYE packet is then
        # scheduled for time tn = tc + T.

        # Every time a BYE packet from another participant is received,
        # members is incremented by 1 regardless of whether that participant
        # exists in the member table or not, and when SSRC sampling is in
        # use, regardless of whether or not the BYE SSRC would be included
        # in the sample.  members is NOT incremented when other RTCP packets
        # or RTP packets are received, but only for BYE packets.  Similarly,
        # avg_rtcp_size is updated only for received BYE packets.  senders
        # is NOT updated when RTP packets arrive; it remains 0.

        # Transmission of the BYE packet then follows the rules for
        # transmitting a regular RTCP packet, as above.
        
        packet = RTCPBYEAlgorithm.create_rtcp_bye_packet(session)
        # TODO to_bytes functions
        RTPSender.send_packet(packet.to_bytes(), session)
        
    @staticmethod
    def create_rtcp_bye_packet(session: RTPSession, reason: str | None = None) -> RTCPBYEPacket:
        # length will be updated when calling the to_bytes data
        packet = RTCPBYEPacket()
        
        packet.header = RTCPHeader()
        packet.header.payload_type = RTPPayloadTypeEnum.RTCP_BYE.value
        packet.header.block_count = 1
        packet.header.ssrc = session.participant.ssrc
        packet.sources = [packet.header.ssrc]
        
        if reason is not None:

            packet.reason = RTCPBYEReason()
            packet.reason.reason = reason
            
        return packet