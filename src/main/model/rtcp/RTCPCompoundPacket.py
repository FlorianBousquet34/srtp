
from main.model.rtcp.RTCPPacket import RTCPPacket


class RTCPCompoundPacket:
    
    def __init__(self, raw_data: bytearray = None) -> None:
        self.raw_data = raw_data
    
    raw_data: bytearray
    
    packets : list[RTCPPacket] = []
    
    def to_bytes(self) -> bytearray:
        
        # first compute lacket bytes and length
        total_length = [0]
        for packet in self.packets:
            total_length.append(total_length[-1] + len(packet.to_bytes()))
        self.raw_data = bytearray(total_length[-1])
        # then parse result
        for index in range(len(self.packets)):
            self.raw_data[total_length[index]: total_length[index + 1]] = self.packets[index].raw_data
        
        return self.raw_data