import unittest
from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtcp.RTCPPacket import RTCPPacket
from main.model.rtcp.RTCPSimpleHeader import RTCPSimpleHeader
from main.model.rtcp.bye.RTCPBYEPacket import RTCPBYEPacket
from main.model.rtcp.bye.RTCPBYEReason import RTCPBYEReason
from main.parser.RTCPParser import RTCPParser
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum

class TestRTPTestCase(unittest.TestCase):
    
    @staticmethod
    def create_bye_packet() -> RTCPBYEPacket:
        
        packet = RTCPBYEPacket()
        packet.header = RTCPSimpleHeader()
        packet.sources = [3125148758, 1456205789]
        packet.reason = RTCPBYEReason()
        packet.reason.reason = "I Want to leave !"
        packet.header.payload_type = RTPPayloadTypeEnum.RTCP_BYE.value
        packet.header.block_count = 2
        
        return packet
    
    def test_build_bye_packet(self):
        
        print("### Test build BYE Packet ###")
        bye_packet = TestRTPTestCase.create_bye_packet()
        packet = RTCPPacket()
        packet.packet = bye_packet
        compound_packet = RTCPCompoundPacket()
        compound_packet.packets = [packet]
        
        compound_packet.to_bytes()
        self.assertIsNotNone(compound_packet.raw_data)
        print(compound_packet.raw_data)
        print("OK")
    
    def test_parse_bye_packet(self):
        
        print("### Test parse BYE Packet ###")
        bye_packet = TestRTPTestCase.create_bye_packet()
        packet = RTCPPacket()
        packet.packet = bye_packet
        compound_packet = RTCPCompoundPacket()
        compound_packet.packets = [packet]
        
        compound_packet.to_bytes()
        parsed_packet = RTCPCompoundPacket(compound_packet.raw_data)
        RTCPParser.parse_rtcp_compound_packet(parsed_packet)
        
        self.assertEqual(len(parsed_packet.packets), 1)
        parsed_bye_packet : RTCPBYEPacket = parsed_packet.packets[0].packet
        self.assertEqual(parsed_bye_packet.reason.reason, bye_packet.reason.reason)
        self.assertEqual(parsed_bye_packet.header.payload_type, RTPPayloadTypeEnum.RTCP_BYE.value)
        self.assertTrue(parsed_bye_packet.header.marker)
        self.assertTrue(parsed_bye_packet.header.padding)
        
        print("OK")
        
        
        

if(__name__ == '__main__'):
    unittest.main()