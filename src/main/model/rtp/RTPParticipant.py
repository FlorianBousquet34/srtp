from main.model.rtcp.RTCPParticipantState import RTCPParticipantState
from main.model.rtp.RTPSession import RTPSession


class RTPParticipant:
    
    def addToSession(self, session : RTPSession):
        self.participantState = RTCPParticipantState(session, self)
        session.sessionMembers.append(self)
    
    # Describes a session participant
    participantState: RTCPParticipantState
    
    # Participant identifier in session ssrc
    ssrc: int