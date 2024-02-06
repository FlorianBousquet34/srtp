from datetime import datetime
import unittest
from main.model.rtp.RTPFixedHeader import RTPFixedHeader
from main.model.rtp.RTPHeader import RTPHeader
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPPayload import RTPPayload
from main.model.rtp.RTPSessionContext import RTPSessionContext
from main.model.srtp.SRTPAuthAlgorithm import SRTPAuthAlgorithm
from main.model.srtp.SRTPAuthMessage import SRTPAuthMessage
from main.model.srtp.SRTPCryptoContext import SRTPCryptoContext
from main.model.srtp.SRTPEncryptAlgorithm import SRTPEncryptAlgorithm

from main.model.srtp.SRTPPacket import SRTPPacket
from main.model.srtp.SRTPSession import SRTPSession
import random

from main.reader.SRTPListenner import SRTPListenner

class TestSRTPTestCase(unittest.TestCase):
    
    @staticmethod
    def create_crypto_context(encrypt_key_length, encrypt_salt_length) -> SRTPCryptoContext:
        
        context : SRTPCryptoContext = SRTPCryptoContext()
        context.auth_algorithm = SRTPAuthAlgorithm()
        context.encrypt_algorithm = SRTPEncryptAlgorithm(encrypt_key_length * 8, encrypt_salt_length * 8)
        
        return context
    
    @staticmethod
    def create_session(crypto_context: SRTPCryptoContext) -> SRTPSession:
        
        session : SRTPSession = SRTPSession(None, crypto_context)
        session.session_encrypt_key = random.SystemRandom().randbytes(crypto_context.encrypt_algorithm.session_key_size // 8)
        session.session_salting_key = random.SystemRandom().randbytes(crypto_context.encrypt_algorithm.session_salt_length // 8)
        session.session_auth_key = random.SystemRandom().randbytes(crypto_context.auth_algorithm.n_a // 8)
        session.session_start = datetime.utcnow()
        
        return session
    
    @staticmethod
    def create_packet(csrc, payload_type, seq_num, timestamp, ssrc, payload) -> SRTPPacket:
        
        packet = SRTPPacket()
        packet.auth_message = SRTPAuthMessage()
        packet.auth_message.rtp_packet = RTPPacket()
        packet.auth_message.rtp_packet.header = RTPHeader()
        packet.auth_message.rtp_packet.header.fixed_header = RTPFixedHeader()
        packet.auth_message.rtp_packet.payload = RTPPayload()
        packet.auth_message.rtp_packet.header.csrc_list = csrc
        packet.auth_message.rtp_packet.header.fixed_header.csrc_number = len(csrc)
        packet.auth_message.rtp_packet.header.fixed_header.payload_type = payload_type
        packet.auth_message.rtp_packet.header.fixed_header.sequence_number = seq_num
        packet.auth_message.rtp_packet.header.fixed_header.timestamp = timestamp
        packet.auth_message.rtp_packet.header.fixed_header.ssrc = ssrc
        packet.auth_message.rtp_packet.payload.payload = payload
        
        return packet
    
    def test_build_parse_packet(self):
        
        print("### Test Valid SRTP Packet ###")
        context = TestSRTPTestCase.create_crypto_context(32, 32)
        session = TestSRTPTestCase.create_session(context)
        
        csrc, payload_type, seq_num, timestamp, ssrc = ([1988265441, 541298968], 79, 37815, 781532197, 87152116)
        payload = "Hello world in a srtp packet!"
        packet : SRTPPacket = TestSRTPTestCase.create_packet(csrc, payload_type, seq_num, timestamp, ssrc, payload)
        packet.to_bytes(session)
        self.assertEqual(len(packet.raw_message) % 4, 0)
        
        parsed_packet = SRTPListenner.read_incoming_srtp_packet(packet.raw_message, session)
        
        self.assertTrue(parsed_packet.authenticated)
        self.assertIsNotNone(packet.auth_message)
        self.assertIsNotNone(packet.auth_tag)
        self.assertIsNotNone(packet.auth_message.rtp_packet)
        self.assertIsNotNone(parsed_packet.auth_message.rtp_packet.header)
        self.assertIsNotNone(parsed_packet.auth_message.rtp_packet.payload)
        self.assertIsNotNone(parsed_packet.auth_message.rtp_packet.header.fixed_header)
        self.assertListEqual(parsed_packet.auth_message.rtp_packet.header.csrc_list, csrc)
        self.assertEqual(parsed_packet.auth_message.rtp_packet.header.fixed_header.payload_type, payload_type)
        self.assertEqual(parsed_packet.auth_message.rtp_packet.header.fixed_header.sequence_number, seq_num)
        self.assertEqual(parsed_packet.auth_message.rtp_packet.header.fixed_header.timestamp, timestamp)
        self.assertEqual(parsed_packet.auth_message.rtp_packet.header.fixed_header.version, 2)
        self.assertTrue(parsed_packet.auth_message.rtp_packet.header.fixed_header.padding)
        self.assertFalse(parsed_packet.auth_message.rtp_packet.header.fixed_header.extension)
        self.assertFalse(parsed_packet.auth_message.rtp_packet.header.fixed_header.marker)
        self.assertEqual(parsed_packet.auth_message.rtp_packet.header.fixed_header.ssrc, ssrc)
        self.assertEqual(parsed_packet.auth_message.rtp_packet.payload.payload, payload)
        
        print("OK")
        
    
if(__name__ == '__main__'):
    unittest.main()