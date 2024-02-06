from main.model.rtcp.RTCPConsts import HEADER_SIZE, IS_ENCRYPTED_MULTIPLIER, SMALL_HEADER_SIZE
from main.model.srtcp.SRTCPCompoundPacket import SRTCPCompoundPacket
from main.model.srtcp.SRTCPPacket import SRTCPPacket
from main.parser.RTCPParser import RTCPParser
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum

SRTCP_INDEX_EXTENSION = 4

class SRTCPParser(RTCPParser):
    
    @staticmethod
    def parse_rtcp_packet(compound_packet: SRTCPCompoundPacket, start_of_packet: int) -> int:
        
        if len(compound_packet.raw_data) >= start_of_packet + SMALL_HEADER_SIZE:
            
            raw_small_header = compound_packet.raw_data[start_of_packet: start_of_packet + SMALL_HEADER_SIZE]
            header = RTCPParser.parse_rtcp_simple_header(raw_small_header)
            payload_start = start_of_packet + SMALL_HEADER_SIZE
            if header.payload_type not in [RTPPayloadTypeEnum.RTCP_BYE.value, RTPPayloadTypeEnum.RTCP_SDES.value]:
                if len(compound_packet.raw_data) >= start_of_packet + HEADER_SIZE:
                    header = RTCPParser.parse_rtcp_header(compound_packet.raw_data[start_of_packet + SMALL_HEADER_SIZE: start_of_packet + HEADER_SIZE], header)
                    payload_start = start_of_packet + HEADER_SIZE
                else:
                    raise ValueError("The RTCP Compound block was too small to read the header")
            
            if len(compound_packet.raw_data) >= start_of_packet + HEADER_SIZE + header.length:
                
                raw_payload = compound_packet.raw_data[payload_start: payload_start + header.length]
                packet, payload_size = RTCPParser.parse_rtcp_payload(raw_payload, header)
                packet = SRTCPPacket(packet)
                srtcp_ext = int.from_bytes(compound_packet.raw_data[payload_start + header.length: payload_start + header.length + 4])
                packet.srtcp_index = srtcp_ext % IS_ENCRYPTED_MULTIPLIER
                packet.is_encrypted = srtcp_ext >= IS_ENCRYPTED_MULTIPLIER
                compound_packet.packets.append(packet)
                
            else:
                
                raise ValueError("The body of the RTCP Packet was smaller than the given length")
        else:
            
            raise ValueError("The RTCP Compound block was too small to read the header")
        
        return payload_size + HEADER_SIZE + SRTCP_INDEX_EXTENSION * 8