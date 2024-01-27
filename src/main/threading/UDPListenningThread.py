import threading

from main.model.rtp.RTPSession import RTPSession
from main.model.srtp.SRTPSession import SRTPSession


class UDPListenningThread(threading.Thread):
    def __init__(self, session):
        
        threading.Thread.__init__(self)
        self.session = session
        self.start()
    
    def run(self):
        
        while not self.interrupt:
            
            packet = self.session.profile.sock.recv(self.session.profile.buffer_size)
            
            if(packet != b''):
                
                self.session.participant.participant_state.handling_thread.lock()
                self.session.participant.participant_state.handling_thread.msg_queue.append(packet)
                self.session.participant.participant_state.handling_thread.unlock()
    
    interrupt: bool = False
    
    session: RTPSession | SRTPSession
    