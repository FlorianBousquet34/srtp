from main.model.rtcp.RTCPParticipantState import RTCPParticipantState
from main.model.rtp.RTPSession import RTPSession


class RTPParticipant:
    
    def __init__(self, ssrc : int) -> None:
        self.ssrc = ssrc
    
    def join_session(self, session : RTPSession):
        
        # Called when the current participant is joining a session
        
        self.participant_state = RTCPParticipantState(session, self)
        session.add_to_session(self.ssrc)
        session.participant = self
    
    # Describes a session participant
    participant_state: RTCPParticipantState
    
    # Participant identifier in session ssrc
    ssrc: int
    
    # Flag activated if a BYE Event was received
    is_leaving : bool = False
    
    # Flag activated is participant is validated in session
    is_validated : bool = False