
import unittest
from main.model.rtp.RTPFixedHeader import RTPFixedHeader
from main.model.rtp.RTPHeader import RTPHeader
import random
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPPayload import RTPPayload
from main.parser.RTPParser import RTPParser


class TestRTPTestCase(unittest.TestCase):
    
    @staticmethod
    def create_packet(csrc, payload_type, seq_num, timestamp, ssrc, payload) -> RTPPacket:
        
        packet = RTPPacket()
        packet.header = RTPHeader()
        packet.header.fixed_header = RTPFixedHeader()
        packet.payload = RTPPayload()
        packet.header.csrc_list = csrc
        packet.header.fixed_header.csrc_number = len(csrc)
        packet.header.fixed_header.payload_type = payload_type
        packet.header.fixed_header.sequence_number = seq_num
        packet.header.fixed_header.timestamp = timestamp
        packet.header.fixed_header.ssrc = ssrc
        packet.payload.payload = payload
        
        return packet
        
    def test_build_packet(self):
        
        print("### Test to byte RTP Packet ###")
        csrc, payload_type, seq_num, timestamp, ssrc = ([1988265441, 541298968], 79, 37815, 781532197, 87152116)
        payload = "Hello world in a rtp packet"
        packet : RTPPacket = TestRTPTestCase.create_packet(csrc, payload_type, seq_num, timestamp, ssrc, payload)
        packet.to_bytes()
        self.assertEqual(len(packet.raw_data) % 4, 0)
        self.assertEqual(bytearray(b'\xa2O\x93\xb7.\x95<%\x051\xd5\xf4v\x82\x85\xe1 C\x91\x18Hello world in a rtp packet\x01'), packet.raw_data)
        print("OK")
        
    def test_parse_packet(self):
        
        print("### Test parsing RTP Packet ###")
        csrc, payload_type, seq_num, timestamp, ssrc = ([random.randint(0,2**32 - 1), random.randint(0,2**32 - 1)], random.randint(0,2**7 - 1),
                                                        random.randint(0,2**16 - 1), random.randint(0,2**32 - 1), random.randint(0,2**32 - 1))
        payload = "Hello world in a rtp packet Hello world in a rtp packet Hello world in a rtp packet Hello world in a rtp packet"
        packet : RTPPacket = TestRTPTestCase.create_packet(csrc, payload_type, seq_num, timestamp, ssrc, payload)
        packet.to_bytes()
        
        parsed_packet = RTPPacket(packet.raw_data)
        RTPParser.parse_rtp_packet(parsed_packet)
        
        self.assertIsNotNone(parsed_packet.header)
        self.assertIsNotNone(parsed_packet.payload)
        self.assertIsNotNone(parsed_packet.header.fixed_header)
        self.assertListEqual(parsed_packet.header.csrc_list, csrc)
        self.assertEqual(parsed_packet.header.fixed_header.payload_type, payload_type)
        self.assertEqual(parsed_packet.header.fixed_header.sequence_number, seq_num)
        self.assertEqual(parsed_packet.header.fixed_header.timestamp, timestamp)
        self.assertEqual(parsed_packet.header.fixed_header.version, 2)
        self.assertTrue(parsed_packet.header.fixed_header.padding)
        self.assertFalse(parsed_packet.header.fixed_header.extension)
        self.assertFalse(parsed_packet.header.fixed_header.marker)
        self.assertEqual(parsed_packet.header.fixed_header.ssrc, ssrc)
        self.assertEqual(parsed_packet.payload.payload, payload)
        print("OK")
    

if(__name__ == '__main__'):
    unittest.main()