import threading

from src.main.model.rtp.RTPSession import RTPSession
from src.main.model.srtp.SRTPSession import SRTPSession
from apscheduler.schedulers.background import BackgroundScheduler

from src.main.scheduler.RTCPScheduler import RTCPScheduler

class UDPListenningThread(threading.Thread):
    def __init__(self, session):
        
        threading.Thread.__init__(self)
        self.session = session
        self.start()
    
    def run(self):
        
        self.session.participant.participant_state.rtcp_scheduler = BackgroundScheduler()
        self.session.leave_scheduler = BackgroundScheduler()
        self.session.leave_scheduler.start()
        self.session.participant.participant_state.rtcp_scheduler.start()
        RTCPScheduler.schedule_next_rtcp_message(self.session.participant.participant_state)
        
        while not self.interrupt:
            
            try:
                packet = self.session.profile.sock.recv(self.session.profile.buffer_size)
            except OSError as e:
                if e.errno == 10038:
                    return
                else:
                    raise e
                                
            if(packet != b''):
                
                self.session.participant.participant_state.handling_thread.lock()
                self.session.participant.participant_state.handling_thread.msg_queue.append(packet)
                self.session.participant.participant_state.handling_thread.unlock()
    
    interrupt: bool = False
    
    session: RTPSession | SRTPSession
    