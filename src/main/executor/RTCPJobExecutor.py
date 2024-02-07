
from datetime import datetime
from main.handler.RTCPBuilder import RTCPBuilder
from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtcp.rr.RTCPRRPacket import RTCPRRPacket
from main.model.rtcp.sr.RTCPSRPacket import RTCPSRPacket
from main.model.rtp.RTPSession import RTPSession
from main.sender.RTPSender import RTPSender


class RTCPJobExecutor:
    
    @staticmethod
    def execute_rtcp_jobs(session : RTPSession):
        from main.scheduler.RTCPScheduler import RTCPScheduler

        # Do the computation and send an RTCP Compound packet
        # to all participants of the session
        
        sdes = RTCPBuilder.build_sdes_packet(session)
        report_packet : list[RTCPRRPacket | RTCPSRPacket]
        if session.senders.get(session.participant.ssrc, None) is None:
            report_packet = RTCPBuilder.build_rr_packet(session)
        else:
            report_packet = RTCPBuilder.build_sr_packet(session)
        compound_packet = RTCPCompoundPacket()
        compound_packet.packets = [sdes] + report_packet
        RTPSender.send_packet(compound_packet, session)
        
        session.refresh_latest_rtcp_timers()
        session.update_inactive_participants()
        RTCPScheduler.schedule_next_rtcp_message(session.participant.participant_state)
        session.participant.participant_state.tp = (datetime.utcnow() - session.participant.participant_state.participant_join_time).total_seconds()
        session.participant.participant_state.pmembers = len(session.session_members)
        session.participant.participant_state.initial = False