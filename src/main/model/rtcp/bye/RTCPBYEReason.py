class RTCPBYEReason:
    
    def __init__(self, length: int, reason: str) -> None:
        self.length = length
        self.reason = reason
    
    length: int
    
    reason: str