import threading
from time import sleep

from main.model.rtp.RTPSession import RTPSession
from main.model.srtp.SRTPSession import SRTPSession
from main.reader.RTPListenner import RTPListenner
from main.reader.SRTPListenner import SRTPListenner


class UDPHandlingThread(threading.Thread):
    
    def __init__(self, session):
        
        threading.Thread.__init__(self)
        self.session = session
        self.start()
        
    def lock(self):
        
        while(self.queue_lock):
            sleep(self.session.profile.lock_wait_time)
        self.queue_lock = True
    
    def unlock(self):
        self.queue_lock = False
    
    def run(self):
        
        while not self.interrupt:
            
            if(len(self.msg_queue) > 0):
                
                self.lock()
                to_handle : list[bytearray] = self.add_message_to_handle()
                self.unlock()
                
                for message in to_handle:
                    
                    self.handle_message(message)
                    
                self.lock()
                self.remove_handled_message(to_handle)
                self.unlock()
                
            else:
                
                sleep(self.session.profile.lock_wait_time)
            
    def remove_handled_message(self, handled: list[bytearray]):
        
        for msg in handled:
            self.msg_queue.remove(msg)
            
    def add_message_to_handle(self) -> list[bytearray]:
        
        result : list[bytearray] = []
        for msg in self.msg_queue:
            result.append(msg)
            
        return result
    
    def handle_message(self, packet: bytearray):
        
        if isinstance(self.session, RTPSession):
                    
            RTPListenner.read_incoming_rtp_packet(packet, self.session)
                    
        elif isinstance(self.session, SRTPSession):
                    
            SRTPListenner.read_incoming_srtp_packet(packet, self.session)
    
    
    queue_lock : bool = False
    
    msg_queue : list[bytearray] = []
    
    interrupt: bool = False
    
    session: RTPSession | SRTPSession