
from datetime import datetime
from src.main.handler.RTCPBuilder import RTCPBuilder
from src.main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from src.main.model.rtcp.RTCPPacket import RTCPPacket
from src.main.model.rtcp.rr.RTCPRRPacket import RTCPRRPacket
from src.main.model.rtcp.sr.RTCPSRPacket import RTCPSRPacket
from src.main.model.rtp.RTPSession import RTPSession
from src.main.sender.RTPSender import RTPSender


class RTCPJobExecutor:
    
    @staticmethod
    def execute_rtcp_jobs(session : RTPSession):

        from src.main.scheduler.RTCPScheduler import RTCPScheduler

        # Do the computation and send an RTCP Compound packet
        # to all participants of the session
        
        sdes = RTCPBuilder.build_sdes_packet(session)
        report_packets : list[RTCPRRPacket | RTCPSRPacket]
        if session.senders.get(session.participant.ssrc, None) is None:
            report_packets = RTCPBuilder.build_rr_packet(session)
        else:
            report_packets = RTCPBuilder.build_sr_packet(session)
        compound_packet = RTCPCompoundPacket()
        compound_packet.packets = [RTCPPacket(sdes)] + [RTCPPacket(p) for p in report_packets]
        compound_packet.to_bytes()
        RTPSender.send_packet(compound_packet, session)
        
        session.refresh_latest_rtcp_timers()
        session.update_inactive_participants()
        RTCPScheduler.schedule_next_rtcp_message(session.participant.participant_state)
        session.participant.participant_state.tp = (datetime.utcnow() - session.participant.participant_state.participant_join_time).total_seconds()
        session.participant.participant_state.pmembers = len(session.session_members)
        session.participant.participant_state.initial = False