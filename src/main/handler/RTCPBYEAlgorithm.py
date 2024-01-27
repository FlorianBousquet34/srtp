import datetime
from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.bye.RTCPBYEPacket import RTCPBYEPacket
from main.model.rtcp.bye.RTCPBYEReason import RTCPBYEReason
from main.model.rtp.RTPSession import RTPSession
from main.scheduler.RTCPTrsIntervalComputation import RTCPTransmissionIntervalComputation
from main.sender.RTPSender import RTPSender
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum
from apscheduler.schedulers.asyncio import AsyncIOScheduler

SESSION_MEMBERS_THRESHOLD : int = 50

class RTCPBYEAlgorithm:
    
    @staticmethod
    def execute_bye_algorithm(session: RTPSession):
        
        bye_packet = RTCPBYEAlgorithm.create_rtcp_bye_packet(session)
        compound_packet = RTCPCompoundPacket()
        compound_packet.packets = [bye_packet]
        compound_packet.to_bytes()

        # https://datatracker.ietf.org/doc/html/rfc3550#section-6.3.7
        # if the number of members is more than 50 when the participant chooses to
        # leave.  This algorithm usurps the normal role of the members variable
        # to count BYE packets instead:
        if len(session.session_members) > SESSION_MEMBERS_THRESHOLD:
        # When the participant decides to leave the system, tp is reset to
        # tc, the current time, members and pmembers are initialized to 1,
        # initial is set to 1, we_sent is set to false, senders is set to 0,
        # and avg_rtcp_size is set to the size of the compound BYE packet.
        # The calculated interval T is computed.  The BYE packet is then
        # scheduled for time tn = tc + T.
        
            session.participant.participant_state.tp = session.participant.participant_state.get_tc()
            session.participant.participant_state.members = 1
            session.participant.participant_state.initial = True
            session.participant.participant_state.we_send = False
            session.participant.participant_state.average_packet_size = len(compound_packet.raw_data) - 1
            time_interval = RTCPTransmissionIntervalComputation.compute_rtcp_transmission_interval(session.participant.participant_state)
            schedule_time = datetime.timedelta(seconds=time_interval) + datetime.datetime.utcnow()

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
        
            session.waiting_to_leave_50 = True
            rtcp_scheduler : AsyncIOScheduler = session.participant.participant_state.rtcp_scheduler
            
            if session.participant.participant_state.rtcp_job:
                rtcp_scheduler.remove_job(session.participant.participant_state.rtcp_job.id)
            
            session.participant.participant_state.bye_job = rtcp_scheduler.add_job(
                RTPSender.send_packet(compound_packet.raw_data, session), 'date', schedule_time)
        
        else:
            
            RTPSender.send_packet(compound_packet, session)
        
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