from main.model.rtp.RTPFixedHeader import RTPFixedHeader
from main.model.rtp.RTPHeader import RTPHeader
from main.model.rtp.RTPPacket import RTPPacket

HEADER_FIXED_SIZE = 12
CSRC_SIZE = 4

class RTPParser:
    
    @staticmethod
    def parse_rtp_packet(packet: RTPPacket):
        
        packet.header, start_of_payload = RTPParser.parse_rtp_header(packet.raw_data)
        
        packet.payload = RTPParser.parse_rtp_payload(packet.raw_data[start_of_payload:])
        
    @staticmethod
    def parse_rtp_header(raw_data: bytearray) -> (RTPHeader, int):
        
        header = RTPHeader()
        
        if len(raw_data) >= HEADER_FIXED_SIZE:
            
            # parse fixed part
            header.fixed_header = RTPParser.parse_rtp_fixed_header(raw_data[:HEADER_FIXED_SIZE])
            # parse csrc list
            header.csrc_list = [None] * header.fixed_header.csrc_number
            
            if len(raw_data) >= HEADER_FIXED_SIZE + header.fixed_header.csrc_number * CSRC_SIZE:
                
                for csrc_num in range(header.fixed_header.csrc_number):
                    
                    header.csrc_list[csrc_num] = int(raw_data[HEADER_FIXED_SIZE + csrc_num * CSRC_SIZE: HEADER_FIXED_SIZE + (csrc_num + 1) * CSRC_SIZE])
                
            else:
                
                raise ValueError("RTP Packet too small to parse ", header.fixed_header.csrc_number, " csrc") 
        else:
            
            raise ValueError("RTP Packet was too small to parse header ", HEADER_FIXED_SIZE,
                             " octets required, ", len(raw_data), " octets given")
        
        return header, HEADER_FIXED_SIZE + header.fixed_header.csrc_number * CSRC_SIZE
        
    @staticmethod
    def parse_rtp_fixed_header(raw_data: bytearray) -> RTPFixedHeader:
        
        fixed_header = RTPFixedHeader()
        fixed_header.version = int((raw_data >> 1) & 0b11)
        
        if(fixed_header.version == 2):
            
            fixed_header.padding = (raw_data >> 3) & 1 != 0
            fixed_header.extension = (raw_data >> 4) & 1 != 0
            fixed_header.csrc_number = int((raw_data >> 5) & 0b1111)
            fixed_header.marker = (raw_data >> 9) & 1 != 0
            fixed_header.payload_type = int((raw_data >> 10) & 0b1111111)
            fixed_header.sequence_number = raw_data[3]
            fixed_header.timestamp = raw_data[4:8]
            fixed_header.ssrc = raw_data[8:12]
            
        return fixed_header