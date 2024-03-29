from src.main.model.rtcp.RTCPParticipantState import RTCPParticipantState
from src.main.model.rtp.RTPSession import RTPSession


class RTPParticipant:
    
    def __init__(self, ssrc : int, sdes_infos: dict[int, str]) -> None:
        self.ssrc = ssrc
        self.sdes_infos = sdes_infos
    
    def join_session(self, session : RTPSession):
        
        # Called when the current participant is joining a session
        session.participant = self
        session.sdes_info[self.ssrc] = self.sdes_infos
        session.profile.bind_socket()
        session.participant.participant_state = RTCPParticipantState(session, self)
        session.add_to_session(self.ssrc, self)
    
    # Describes a session participant
    participant_state: RTCPParticipantState
    
    # Participant identifier in session ssrc
    ssrc: int
    
    # Flag activated if a BYE Event was received
    is_leaving : bool = False
    
    # Flag activated is participant is validated in session
    is_validated : bool = False
    
    # SDES infos (includes at least CNAME)
    sdes_infos : dict[int, str]
    
     
    # current roll over count for sequence number
    roc: int = 0