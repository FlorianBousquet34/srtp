from main.model.rtcp.RTCPParticipantState import RTCPParticipantState
from main.model.rtp.RTPSession import RTPSession


class RTPParticipant:
    
    def __init__(self, ssrc : int) -> None:
        self.ssrc = ssrc
    
    def joinSession(self, session : RTPSession):
        
        # Called when the current participant is joining a session
        
        self.participantState = RTCPParticipantState(session, self)
        session.addToSession(self.ssrc)
        session.participant = self
    
    # Describes a session participant
    participantState: RTCPParticipantState
    
    # Participant identifier in session ssrc
    ssrc: int
    
    # Flag activated if a BYE Event was received
    isLeaving : bool = False
    
    # Flag activated is participant is validated in session
    isValidated : bool = False