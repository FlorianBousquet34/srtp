import socket
from time import sleep
from typing import Any
import unittest
from src.main.handler.RTCPBYEAlgorithm import RTCPBYEAlgorithm
from src.main.model.rtcp.sdes.items.RTCPItemEnum import RTCPItemEnum
from src.main.model.rtp.RTPParticipant import RTPParticipant
import random

from src.main.model.rtp.RTPSession import RTPSession
from src.main.model.rtp.RTPSessionContext import RTPSessionContext

class TestRTPSessionTestCase(unittest.TestCase):
    
    
    @staticmethod
    def create_participant(ssrc: int, sdes_info: dict = {}):
            from src.main.model.rtp.RTPParticipant import RTPParticipant
            participant = RTPParticipant(ssrc, sdes_info)
            
            return participant
    
    @staticmethod
    def create_session(profile: RTPSessionContext) -> RTPSession:
        
        session : RTPSession = RTPSession(profile)
        
        return session
    
    def test_openning_rtp_session(self):
        
        ssrc_1 = random.randint(1, 2**31 - 1)
        ssrc_2 = random.randint(2**31, 2**32 - 1)
        address = "127.0.0.1"
        port_1 = 8080
        port_2 = 9090
        sdes_info_participant_1 = {RTCPItemEnum.CNAME.value: address + ":" + str(port_1)}
        sdes_info_participant_2 = {RTCPItemEnum.CNAME.value: address + ":" + str(port_2)}
        context_1: RTPSessionContext = RTPSessionContext(address, port_1)
        context_2: RTPSessionContext = RTPSessionContext(address, port_2)
        session_1: RTPSession = TestRTPSessionTestCase.create_session(context_1)
        session_2: RTPSession = TestRTPSessionTestCase.create_session(context_2)
        participant_1 : RTPParticipant = TestRTPSessionTestCase.create_participant(ssrc_1, sdes_info_participant_1)
        participant_1.join_session(session_1)
        participant_2 : RTPParticipant = TestRTPSessionTestCase.create_participant(ssrc_2, sdes_info_participant_2)
        participant_2.join_session(session_2)
        session_1.add_to_session(ssrc_2, participant_2)
        session_2.add_to_session(ssrc_1, participant_1)
        
        sleep(6)
        
        RTCPBYEAlgorithm.execute_bye_algorithm(session_1)
        RTCPBYEAlgorithm.execute_bye_algorithm(session_2)
        
        # les infos sdes ont bien été ajoutés
        self.assertEqual(session_1.sdes_info[ssrc_2], {RTCPItemEnum.CNAME.value: address + ":" + str(port_2)})
        self.assertEqual(session_2.sdes_info[ssrc_1], {RTCPItemEnum.CNAME.value: address + ":" + str(port_1)})
        
        # les threads ont été arreté
        self.assertTrue(session_1.participant.participant_state.listenning_thread.interrupt)
        self.assertTrue(session_2.participant.participant_state.listenning_thread.interrupt)
    
if(__name__ == '__main__'):
    unittest.main()