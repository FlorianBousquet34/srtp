import random
import unittest
from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.RTCPPacket import RTCPPacket
from main.model.rtcp.RTCPSimpleHeader import RTCPSimpleHeader
from main.model.rtcp.app.RTCPAPPPacket import RTCPAPPPacket
from main.model.rtcp.bye.RTCPBYEPacket import RTCPBYEPacket
from main.model.rtcp.bye.RTCPBYEReason import RTCPBYEReason
from main.model.rtcp.r.RTCPReportBlock import RTCPReportBlock
from main.model.rtcp.rr.RTCPRRPacket import RTCPRRPacket
from main.model.rtcp.sdes.RTCPSDESChunk import RTCPSDEChunk
from main.model.rtcp.sdes.RTCPSDESPacket import RTCPSDESPacket
from main.model.rtcp.sdes.items.RTCPGenericItem import RTCPGenericItem
from main.model.rtcp.sdes.items.RTCPItemEnum import RTCPItemEnum
from main.model.rtcp.sr.RTCPSRPacket import RTCPSRPacket
from main.model.rtcp.sr.RTCPSRSenderInfo import RTCPSRSenderInfo
from main.parser.RTCPParser import RTCPParser
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum

class TestRTCPTestCase(unittest.TestCase):
    
    @staticmethod
    def create_bye_packet() -> RTCPBYEPacket:
        
        packet = RTCPBYEPacket()
        packet.header = RTCPSimpleHeader()
        packet.sources = [random.randint(0, 2**32 - 1), random.randint(0, 2**32 - 1)]
        packet.reason = RTCPBYEReason()
        packet.reason.reason = "I Want to leave !"
        packet.header.payload_type = RTPPayloadTypeEnum.RTCP_BYE.value
        packet.header.block_count = 2
        
        return packet
    
    @staticmethod
    def create_sdes_packet() -> RTCPSDESPacket:
        
        packet = RTCPSDESPacket()
        packet.header = RTCPSimpleHeader()
        packet.header.payload_type = RTPPayloadTypeEnum.RTCP_SDES.value
        packet.header.block_count = random.randint(0, 31)
        packet.chuncks = [RTCPSDEChunk() for _ in range(packet.header.block_count)]
        for ck in packet.chuncks:
            ck.source = random.randint(0, 2**32 - 1)
            ck.sdes_items = [RTCPGenericItem(), RTCPGenericItem(), RTCPGenericItem()]
            ck.sdes_items[0].sdes_key = RTCPItemEnum.CNAME
            ck.sdes_items[0].sdes_value = ".".join([str(random.randint(0,256))]*4) + ":" + str(random.randint(0,9999))
            ck.sdes_items[1].sdes_key = RTCPItemEnum.NAME
            ck.sdes_items[1].sdes_value = "testeur_" + str(random.randint(0, 256))
            ck.sdes_items[2].sdes_key = RTCPItemEnum.EMAIL
            ck.sdes_items[2].sdes_value = "testeur_" + str(random.randint(0, 256)) + "@test.com"
        
        return packet
    
    @staticmethod
    def create_rr_packet() -> RTCPRRPacket:
        
        packet = RTCPRRPacket()
        packet.header = RTCPHeader()
        packet.header.ssrc = random.randint(0, 2**32 - 1)
        packet.header.payload_type = RTPPayloadTypeEnum.RTCP_RR.value
        packet.header.block_count = random.randint(0, 31)
        packet.reports = [RTCPReportBlock() for _ in range(packet.header.block_count)]
        for i_r in range(packet.header.block_count):
            report = packet.reports[i_r]
            report.ssrc = random.randint(0, 2**32 - 1)
            report.last_sr_timestamp = random.randint(0, 2**32 - 1)
            report.interarrival_jitter = random.randint(0, 2**32 - 1)
            report.fraction_lost = random.randint(0, 2**8 - 1)
            report.ext_highest_seq_num_received = random.randint(0, 2**32 - 1)
            report.delay_last_sr = random.randint(0, 2**32 - 1)
            report.cumul_packet_lost = random.randint(0, 2**24 - 1)
        
        return packet
    
    @staticmethod
    def create_sr_packet() -> RTCPSRPacket:
        
        packet = RTCPSRPacket()
        packet.header = RTCPHeader()
        packet.header.ssrc = random.randint(0, 2**32 - 1)
        packet.header.payload_type = RTPPayloadTypeEnum.RTCP_SR.value
        packet.header.block_count = random.randint(0, 31)
        packet.sender_info = RTCPSRSenderInfo()
        packet.sender_info.ntp_timestamp = random.randint(0, 2**64-1)
        packet.sender_info.rtp_timestamp = random.randint(0, 2**32 -1)
        packet.sender_info.sender_octet_count = random.randint(0, 2**32 -1)
        packet.sender_info.sender_packet_count = random.randint(0, 2**32 -1)
        packet.reports = [RTCPReportBlock() for _ in range(packet.header.block_count)]
        for i_r in range(packet.header.block_count):
            report = packet.reports[i_r]
            report.ssrc = random.randint(0, 2**32 - 1)
            report.last_sr_timestamp = random.randint(0, 2**32 - 1)
            report.interarrival_jitter = random.randint(0, 2**32 - 1)
            report.fraction_lost = random.randint(0, 2**8 - 1)
            report.ext_highest_seq_num_received = random.randint(0, 2**32 - 1)
            report.delay_last_sr = random.randint(0, 2**32 - 1)
            report.cumul_packet_lost = random.randint(0, 2**24 - 1)
        
        return packet
        
        
    @staticmethod
    def create_app_packet() -> RTCPAPPPacket:
        
        packet = RTCPAPPPacket()
        packet.header = RTCPHeader()
        packet.header.ssrc = 1235263789
        packet.header.payload_type = RTPPayloadTypeEnum.RTCP_APP.value
        packet.name = "aaaa"
        packet.data = "a message readable by my app".encode()
        
        return packet
    
    def test_build_parse_bye_packet(self):
        
        print("### Test parse BYE Packet ###")
        bye_packet = TestRTCPTestCase.create_bye_packet()
        packet = RTCPPacket()
        packet.packet = bye_packet
        compound_packet = RTCPCompoundPacket()
        compound_packet.packets = [packet]
        
        compound_packet.to_bytes()
        self.assertIsNotNone(compound_packet.raw_data)
        
        parsed_packet = RTCPCompoundPacket(compound_packet.raw_data)
        RTCPParser.parse_rtcp_compound_packet(parsed_packet)
        
        self.assertEqual(len(parsed_packet.packets), 1)
        parsed_bye_packet : RTCPBYEPacket = parsed_packet.packets[0].packet
        self.assertEqual(parsed_bye_packet.reason.reason, bye_packet.reason.reason)
        self.assertEqual(parsed_bye_packet.header.payload_type, RTPPayloadTypeEnum.RTCP_BYE.value)
        self.assertTrue(parsed_bye_packet.header.marker)
        
        print("OK")
        
    def test_build_parse_app_packet(self):
        
        print("### Test build APP Packet ###")
        app_packet = TestRTCPTestCase.create_app_packet()
        packet = RTCPPacket()
        packet.packet = app_packet
        c_p = RTCPCompoundPacket()
        c_p.packets = [packet]
        c_p.to_bytes()
        self.assertIsNotNone(c_p.raw_data)
        parsed_packet = RTCPCompoundPacket(c_p.raw_data)
        RTCPParser.parse_rtcp_compound_packet(parsed_packet)
        
        self.assertEqual(len(parsed_packet.packets), 1)
        parsed_app_packet : RTCPAPPPacket = parsed_packet.packets[0].packet
        self.assertEqual(parsed_app_packet.header.payload_type, RTPPayloadTypeEnum.RTCP_APP.value)
        self.assertTrue(parsed_app_packet.header.marker)
        self.assertEqual(app_packet.header.ssrc, parsed_app_packet.header.ssrc)
        self.assertEqual(app_packet.name, parsed_app_packet.name)
        self.assertEqual(app_packet.data, parsed_app_packet.data)
        
        print("OK")
        
    def test_build_parse_sdes_packet(self):
        
        print("### Test build SDES Packet ###")
        sdes_packet = TestRTCPTestCase.create_sdes_packet()
        packet = RTCPPacket()
        packet.packet = sdes_packet
        c_p = RTCPCompoundPacket()
        c_p.packets = [packet]
        c_p.to_bytes()
        self.assertIsNotNone(c_p.raw_data)
        
        parsed_c_p = RTCPCompoundPacket(c_p.raw_data)
        RTCPParser.parse_rtcp_compound_packet(parsed_c_p)
        self.assertEqual(len(parsed_c_p.packets), 1)
        parsed_sdes : RTCPSDESPacket = parsed_c_p.packets[0].packet
        self.assertEqual(len(parsed_sdes.chuncks), len(sdes_packet.chuncks))
        self.assertEqual(parsed_sdes.header.block_count, sdes_packet.header.block_count)
        self.assertEqual(parsed_sdes.header.payload_type, RTPPayloadTypeEnum.RTCP_SDES.value)
        self.assertTrue(parsed_sdes.header.marker)
        for i_ck, ck in enumerate(parsed_sdes.chuncks):
            self.assertEqual(len(ck.sdes_items), 3)
            self.assertEqual(ck.source, sdes_packet.chuncks[i_ck].source)
            self.assertEqual(ck.sdes_items[0].sdes_key, RTCPItemEnum.CNAME)
            self.assertEqual(ck.sdes_items[1].sdes_key, RTCPItemEnum.NAME)
            self.assertEqual(ck.sdes_items[2].sdes_key, RTCPItemEnum.EMAIL)
            self.assertEqual(ck.sdes_items[0].sdes_value, sdes_packet.chuncks[i_ck].sdes_items[0].sdes_value)
            self.assertEqual(ck.sdes_items[1].sdes_value, sdes_packet.chuncks[i_ck].sdes_items[1].sdes_value)
            self.assertEqual(ck.sdes_items[2].sdes_value, sdes_packet.chuncks[i_ck].sdes_items[2].sdes_value)
        
        print("OK")
        
    def test_build_parse_rr_packet(self):
        
        print("### Test build RR Packet ###")
        rr_packet = TestRTCPTestCase.create_rr_packet()
        packet = RTCPPacket()
        packet.packet = rr_packet
        c_p = RTCPCompoundPacket()
        c_p.packets = [packet]
        c_p.to_bytes()
        self.assertIsNotNone(c_p.raw_data)
        parsed_c_p = RTCPCompoundPacket(c_p.raw_data)
        RTCPParser.parse_rtcp_compound_packet(parsed_c_p)
        self.assertEqual(len(parsed_c_p.packets), 1)
        parsed_rr : RTCPRRPacket = parsed_c_p.packets[0].packet
        self.assertEqual(parsed_rr.header.block_count, rr_packet.header.block_count)
        self.assertEqual(len(parsed_rr.reports), len(rr_packet.reports))
        self.assertEqual(parsed_rr.header.payload_type, RTPPayloadTypeEnum.RTCP_RR.value)
        self.assertTrue(parsed_rr.header.marker)
        self.assertEqual(parsed_rr.header.ssrc, rr_packet.header.ssrc)
        for i_r, rb in enumerate(parsed_rr.reports):
            org_rb = rr_packet.reports[i_r]
            self.assertEqual(rb.ssrc, org_rb.ssrc)
            self.assertEqual(rb.last_sr_timestamp, org_rb.last_sr_timestamp)
            self.assertEqual(rb.interarrival_jitter, org_rb.interarrival_jitter)
            self.assertEqual(rb.fraction_lost, org_rb.fraction_lost)
            self.assertEqual(rb.ext_highest_seq_num_received, org_rb.ext_highest_seq_num_received)
            self.assertEqual(rb.delay_last_sr, org_rb.delay_last_sr)
            self.assertEqual(rb.cumul_packet_lost, org_rb.cumul_packet_lost)
            
        print("OK")
        
    def test_build_parse_sr_packet(self):
        
        print("### Test build SR Packet ###")
        sr_packet = TestRTCPTestCase.create_sr_packet()
        packet = RTCPPacket()
        packet.packet = sr_packet
        c_p = RTCPCompoundPacket()
        c_p.packets = [packet]
        c_p.to_bytes()
        self.assertIsNotNone(c_p.raw_data)
        parsed_c_p = RTCPCompoundPacket(c_p.raw_data)
        RTCPParser.parse_rtcp_compound_packet(parsed_c_p)
        self.assertEqual(len(parsed_c_p.packets), 1)
        parsed_sr : RTCPSRPacket = parsed_c_p.packets[0].packet
        self.assertEqual(parsed_sr.header.block_count, sr_packet.header.block_count)
        self.assertEqual(len(parsed_sr.reports), len(sr_packet.reports))
        self.assertEqual(parsed_sr.header.payload_type, RTPPayloadTypeEnum.RTCP_SR.value)
        self.assertTrue(parsed_sr.header.marker)
        self.assertEqual(parsed_sr.header.ssrc, sr_packet.header.ssrc)
        self.assertEqual(parsed_sr.sender_info.ntp_timestamp, sr_packet.sender_info.ntp_timestamp)
        self.assertEqual(parsed_sr.sender_info.rtp_timestamp, sr_packet.sender_info.rtp_timestamp)
        self.assertEqual(parsed_sr.sender_info.sender_octet_count, sr_packet.sender_info.sender_octet_count)
        self.assertEqual(parsed_sr.sender_info.sender_packet_count, sr_packet.sender_info.sender_packet_count)
        for i_r, rb in enumerate(parsed_sr.reports):
            org_rb = sr_packet.reports[i_r]
            self.assertEqual(rb.ssrc, org_rb.ssrc)
            self.assertEqual(rb.last_sr_timestamp, org_rb.last_sr_timestamp)
            self.assertEqual(rb.interarrival_jitter, org_rb.interarrival_jitter)
            self.assertEqual(rb.fraction_lost, org_rb.fraction_lost)
            self.assertEqual(rb.ext_highest_seq_num_received, org_rb.ext_highest_seq_num_received)
            self.assertEqual(rb.delay_last_sr, org_rb.delay_last_sr)
            self.assertEqual(rb.cumul_packet_lost, org_rb.cumul_packet_lost)
            
        print("OK")

if(__name__ == '__main__'):
    unittest.main()