from main.model.rtcp.RTCPConsts import DELAY_MULTIPLIER, NTP_TIMESTAMP_MULTIPLIER, OFFSET_OCTETS, REPORT_BLOCK_LIMIT, REPORT_BLOCK_SIZE, SENDER_INFO_SIZE, SEQ_NUM_SIZE
from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.RTCPSimpleHeader import RTCPSimpleHeader
from main.model.rtcp.r.RTCPReportBlock import RTCPReportBlock
from main.model.rtcp.rr.RTCPRRPacket import RTCPRRPacket
from main.model.rtcp.sdes.RTCPSDESChunk import RTCPSDEChunk
from main.model.rtcp.sdes.RTCPSDESPacket import RTCPSDESPacket
from main.model.rtcp.sdes.items.RTCPGenericItem import RTCPGenericItem
from main.model.rtcp.sr.RTCPSRPacket import RTCPSRPacket
from main.model.rtcp.sr.RTCPSRSenderInfo import RTCPSRSenderInfo
from main.model.rtp.RTPPacket import RTPPacket
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum
import random
from main.model.rtp.RTPSession import RTPSession

class RTCPBuilder:
    
    @staticmethod
    def build_sdes_packet(session: RTPSession) -> RTCPSDESPacket:
        
        packet = RTCPSDESPacket()
        packet.header = RTCPBuilder.build_simple_header(RTPPayloadTypeEnum.RTCP_SDES)
        
        chunck = RTCPSDEChunk()
        chunck.source = session.participant.ssrc
        chunck.sdes_items = [RTCPGenericItem() for _ in range(len(session.participant.sdes_infos))]
        item_num = 0
        for item_key in session.participant.sdes_infos:
            
            chunck.sdes_items[item_num].sdes_key = item_key
            chunck.sdes_items[item_num].sdes_value = session.participant.sdes_infos[item_key]
            
        packet.chuncks = [chunck]
        packet.header.block_count = len(packet.chuncks)
        
        return packet
    
    @staticmethod
    def build_rr_packet(session : RTPSession, stacket_length: int = OFFSET_OCTETS) -> list[RTCPRRPacket]:
        
        packet = RTCPRRPacket()
        packet.header = RTCPBuilder.build_header(session, RTPPayloadTypeEnum.RTCP_RR)
        packet.reports = RTCPBuilder.build_rtcp_reports(session)
        packet.profil_specific_data = RTCPBuilder.build_rtcp_profile_specific_data(session, False)
        
        new_length = stacket_length + len(packet.profil_specific_data) + REPORT_BLOCK_SIZE * REPORT_BLOCK_LIMIT
        estimated_next_length = new_length + len(packet.profil_specific_data) + REPORT_BLOCK_SIZE * REPORT_BLOCK_LIMIT
        
        packet.header.block_count = len(packet.reports)
        
        if len(session.lastest_received) > 0 and session.profile.buffer_size <  estimated_next_length:
            return [packet] + RTCPBuilder.build_rr_packet(session, new_length)
        else:
            return [packet]
    
    @staticmethod
    def build_sr_packet(session: RTPSession) -> list[RTCPSRPacket | RTCPRRPacket]:
        
        packet = RTCPSRPacket()
        packet.header = RTCPBuilder.build_header(session, RTPPayloadTypeEnum.RTCP_SR)
        
        packet.reports = RTCPBuilder.build_rtcp_reports(session)
        packet.sender_info = RTCPBuilder.build_rtcp_sender_info(session)
        packet.profil_specific_data = RTCPBuilder.build_rtcp_profile_specific_data(session, True)
        
        packet.header.block_count = len(packet.reports)
        
        if len(session.lastest_received) > 0:
            return [packet] + RTCPBuilder.build_rr_packet(session, OFFSET_OCTETS + SENDER_INFO_SIZE + len(packet.profil_specific_data) + REPORT_BLOCK_SIZE * REPORT_BLOCK_LIMIT)
        else:
            return [packet]
    
    @staticmethod
    def build_rtcp_sender_info(session: RTPSession) -> RTCPSRSenderInfo:
        
        info = RTCPSRSenderInfo()
        info.ntp_timestamp = session.get_ntp_timestamp()
        info.rtp_timestamp = session.participant.participant_state.get_rtp_timestamp()
        info.sender_packet_count = len(session.latest_sent)
        info.sender_octet_count = RTCPBuilder.compute_rtp_octet_count(session.latest_sent)
        
        return info
    
    @staticmethod
    def build_rtcp_profile_specific_data(session : RTPSession, is_sender: bool) -> bytearray:
        
        # !!! Overide this method to build specific profile data
        
        return bytearray()
    
    @staticmethod
    def build_header(session: RTPSession, payload_type: RTPPayloadTypeEnum) -> RTCPHeader:
        
        simple_header = RTCPBuilder.build_simple_header(payload_type)
        header = RTCPHeader(simple_header)
        header.ssrc = session.participant.ssrc
        header.block_count = 1
        
        return header
    
    @staticmethod
    def build_simple_header(payload_type: RTPPayloadTypeEnum) -> RTCPSimpleHeader:
        
        header = RTCPSimpleHeader()
        header.payload_type = payload_type.value
        header.block_count = 1
        header.length = 0
        
        return header
    
    @staticmethod
    def compute_rtp_octet_count(packets: list[RTPPacket]) -> int:
        
        return sum([packet.payload.payload for packet in packets])
    
    @staticmethod
    def build_rtcp_reports(session: RTPSession) -> list[RTCPReportBlock]:
        
        source_num = 0
        reports = [RTCPReportBlock() for _ in range(min(REPORT_BLOCK_LIMIT, len(session.lastest_received)))]
        randomize_key = False
        if len(reports) == REPORT_BLOCK_LIMIT:
            randomize_key = True
        while source_num < REPORT_BLOCK_LIMIT and source_num < len(session.lastest_received): 
            
            if randomize_key:
                reports[source_num].ssrc = random.choices(session.lastest_received.keys())
            else:
                reports[source_num].ssrc = session.lastest_received.keys()[source_num]
            
            RTCPBuilder.compute_rapport_loss(
                session.lastest_received[reports[source_num].ssrc],
                session,
                reports[source_num])
            
            reports[source_num].last_sr_timestamp = int(session.latest_sr_report.get(reports[source_num].ssrc, (0,0))[0])
            current_ntp_timestamp = session.get_ntp_timestamp()
            reports[source_num].delay_last_sr = ((current_ntp_timestamp - int(session.latest_sr_report.get(reports[source_num].ssrc, (0,current_ntp_timestamp))[1]))
                                                    // NTP_TIMESTAMP_MULTIPLIER ) * DELAY_MULTIPLIER
            reports[source_num].interarrival_jitter = session.interarrival_jitter.get(reports[source_num].ssrc, 0)
            
            
            source_num += 1
        
        # clear threated sources
        for report in reports:
            session.lastest_received.pop(report.ssrc)
        
        return reports
    
    @staticmethod
    def compute_rapport_loss(packets: list[RTPPacket], session : RTPSession, report: RTCPReportBlock):
        
        max_seq_num = max([packet.header.fixed_header.sequence_number for packet in packets])
        min_seq_num = min([[packet.header.fixed_header.sequence_number for packet in packets]])
        # first detect if sequence was reset
        if max_seq_num - min_seq_num > SEQ_NUM_SIZE // 2:
            # Caution TO FIX : Late packet migth trigger dulicate sequence roll
            # second compute extended seq num
            extended_seq_num = [packet.header.fixed_header.sequence_number + SEQ_NUM_SIZE * session.seq_num_roll.get(report.ssrc, 0)
                                if packet.header.fixed_header.sequence_number > SEQ_NUM_SIZE // 2
                                else packet.header.fixed_header.sequence_number + SEQ_NUM_SIZE * (session.seq_num_roll.get(report.ssrc, 0) + 1)
                                for packet in packets]
            session.increase_roc(report.ssrc, max([packet.header.fixed_header.sequence_number
                                                   for packet in packets
                                                   if packet.header.fixed_header.sequence_number < SEQ_NUM_SIZE // 2]))
        else:
            extended_seq_num = [packet.header.fixed_header.sequence_number + SEQ_NUM_SIZE * session.seq_num_roll.get(report.ssrc, 0) for packet in packets]
        
        report.ext_highest_seq_num_received = max(extended_seq_num)
        report.cumul_packet_lost = max(extended_seq_num) - min(extended_seq_num)
        report.fraction_lost = max(0, min(255,int(len(packets) / report.cumul_packet_lost * 256)))