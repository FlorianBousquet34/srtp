from main.model.rtp.RTPFixedHeader import RTPFixedHeader
from main.model.rtp.RTPHeader import RTPHeader
from main.model.rtp.RTPHeaderExtension import RTPHeaderExtension
from main.model.rtp.RTPPacket import RTPPacket
from main.model.rtp.RTPPayload import RTPPayload

HEADER_FIXED_SIZE = 12
CSRC_SIZE = 4

class RTPParser:
    
    @staticmethod
    def parse_rtp_packet(packet: RTPPacket):
        
        packet.header = RTPHeader()
        start_of_payload = RTPParser.parse_rtp_header(packet.raw_data, packet.header)
        
        packet.payload = RTPParser.parse_rtp_payload(packet.raw_data[start_of_payload:], packet.header.fixed_header.padding)
        
    @staticmethod
    def parse_rtp_header(raw_data: bytearray, header: RTPHeader) -> int:
        
        extension_offset = 0
        if len(raw_data) >= HEADER_FIXED_SIZE:
            
            # parse fixed part
            header.fixed_header = RTPParser.parse_rtp_fixed_header(raw_data[:HEADER_FIXED_SIZE])
            # parse csrc list
            header.csrc_list = [0] * header.fixed_header.csrc_number
            
            if len(raw_data) >= HEADER_FIXED_SIZE + header.fixed_header.csrc_number * CSRC_SIZE:
                
                for csrc_num in range(header.fixed_header.csrc_number):
                    
                    header.csrc_list[csrc_num] = int.from_bytes(raw_data[HEADER_FIXED_SIZE + csrc_num * CSRC_SIZE: HEADER_FIXED_SIZE + (csrc_num + 1) * CSRC_SIZE])
                    
            if header.fixed_header.extension:
                
                header.header_extension = RTPHeaderExtension()
                extension_offset = RTPParser.parse_rtp_header_extension(header.header_extension, raw_data[HEADER_FIXED_SIZE + header.fixed_header.csrc_number * CSRC_SIZE:])
                
            else:
                
                raise ValueError("RTP Packet too small to parse ", header.fixed_header.csrc_number, " csrc") 
        else:
            
            raise ValueError("RTP Packet was too small to parse header ", HEADER_FIXED_SIZE,
                             " octets required, ", len(raw_data), " octets given")
        
        return HEADER_FIXED_SIZE + header.fixed_header.csrc_number * CSRC_SIZE + extension_offset
    
    @staticmethod
    def parse_rtp_header_extension(extension: RTPHeaderExtension, raw_data: bytearray) -> int:
        
        extension.extension_implem_identifier = int.from_bytes(raw_data[:2])
        extension.length = int.from_bytes(raw_data[2:4])
        extension.text = raw_data[4: 4 + extension.length * 4]
        
        return 4 + extension.length * 4
        
    @staticmethod
    def parse_rtp_fixed_header(raw_data: bytearray) -> RTPFixedHeader:
        
        fixed_header = RTPFixedHeader()
        fixed_header.version = (raw_data[0] >> 6) & 0b11
        
        if(fixed_header.version == 2):
            
            fixed_header.padding = (raw_data[0] >> 3) & 1 != 0
            fixed_header.extension = (raw_data[0] >> 5) & 1 != 0
            fixed_header.csrc_number = raw_data[0] & 0b1111
            fixed_header.marker = (raw_data[1] >> 7) & 1 != 0
            fixed_header.payload_type = raw_data & 0b1111111
            fixed_header.sequence_number = int.from_bytes(raw_data[2:4])
            fixed_header.timestamp = int.from_bytes(raw_data[4:8])
            fixed_header.ssrc = int.from_bytes(raw_data[8:12])
            
        return fixed_header
    
    @staticmethod
    def parse_rtp_payload(data: bytearray, is_padded: bool) -> RTPPayload:
        
        unpadded_data = data
        pad_count = 0
        
        if is_padded:
            
            pad_count = data[-1]
            unpadded_data = data[: - pad_count]
        
        payload = RTPPayload()
        payload.payload = unpadded_data.decode()
        payload.pad_count = pad_count
        payload.raw_payload = data
        
        return payload
        