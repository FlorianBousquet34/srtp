from typing import Tuple
from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtcp.RTCPConsts import HEADER_SIZE, REPORT_BLOCK_SIZE, SENDER_INFO_SIZE, SMALL_HEADER_SIZE, SSRC_SIZE
from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.RTCPPacket import RTCPPacket
from main.model.rtcp.RTCPSimpleHeader import RTCPSimpleHeader
from main.model.rtcp.app.RTCPAPPPacket import RTCPAPPPacket
from main.model.rtcp.bye.RTCPBYEPacket import RTCPBYEPacket
from main.model.rtcp.bye.RTCPBYEReason import RTCPBYEReason
from main.model.rtcp.r.RTCPReportBlock import RTCPReportBlock
from main.model.rtcp.rr.RTCPRRPacket import RTCPRRPacket
from main.model.rtcp.sdes.RTCPSDESChunk import RTCPSDEChunk
from main.model.rtcp.sdes.RTCPSDESPacket import RTCPSDESPacket
from main.model.rtcp.sdes.items.RTCPGenericItem import RTCPGenericItem
from main.model.rtcp.sdes.items.RTCPItemEnum import RTCPItemEnum
from main.model.rtcp.sr.RTCPSRPacket import RTCPSRPacket
from main.model.rtcp.sr.RTCPSRSenderInfo import RTCPSRSenderInfo
from main.utils.enum.RTPPayloadTypeEnum import RTPPayloadTypeEnum



class RTCPParser:
    
    @staticmethod
    def parse_rtcp_compound_packet(packet: RTCPCompoundPacket):
        
        if len(packet.raw_data) >= SMALL_HEADER_SIZE:
            
            raw_small_header = packet.raw_data[:SMALL_HEADER_SIZE]
            header = RTCPParser.parse_rtcp_simple_header(raw_small_header)
            
            start_of_packet = 0
            if header.payload_type not in [RTPPayloadTypeEnum.RTCP_BYE.value, RTPPayloadTypeEnum.RTCP_SDES.value]:
                if len(packet.raw_data) >= HEADER_SIZE:
                    header = RTCPParser.parse_rtcp_header(packet.raw_data[SMALL_HEADER_SIZE:HEADER_SIZE], header)
                else:
                    raise ValueError("The RTCP Compound packet received is too small, header could not be parse.")
            
            packet.packets = []
            
            while start_of_packet < len(packet.raw_data):
            
                start_of_packet = RTCPParser.parse_rtcp_packet(packet, start_of_packet)

        else:
            raise ValueError("The RTCP Compound packet received is too small, header could not be parse.")
        
        
    @staticmethod
    def parse_rtcp_packet(compound_packet: RTCPCompoundPacket, start_of_packet: int) -> int:

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
            
            if len(compound_packet.raw_data) >= start_of_packet + (header.length + 1) * 4:
                
                raw_payload = compound_packet.raw_data[payload_start: payload_start + header.length * 4]
                packet, payload_size = RTCPParser.parse_rtcp_payload(raw_payload, header)
                compound_packet.packets.append(packet)
                
            else:
                
                raise ValueError("The body of the RTCP Packet was smaller than the given length")
        else:
            
            raise ValueError("The RTCP Compound block was too small to read the header")

        return payload_size + payload_start
    
    @staticmethod
    def parse_rtcp_header(raw_header: bytearray, simple_header: RTCPSimpleHeader) -> RTCPHeader:
        
        header = RTCPHeader(simple_header)
        header.ssrc = int.from_bytes(raw_header)
        return header
    
    @staticmethod
    def parse_rtcp_simple_header(raw_header: bytearray) -> RTCPSimpleHeader:
        
        header = RTCPSimpleHeader()
        header.version = (raw_header[0] >> 6) & 0b11
        
        if header.version == 2:
            
            header.length = int.from_bytes(raw_header[2:4])
            header.padding = (raw_header[0] >> 5) & 1 != 0
            header.block_count = raw_header[0] & 0b11111
            header.payload_type = raw_header[1] >> 0 & 0b1111111
            
        else:
            raise ValueError("The RTCP Compound packed was not well formated, It must contain 4 octets blocks")

        return header
    
    @staticmethod
    def parse_rtcp_payload(raw_payload: bytearray, header: (RTCPHeader | RTCPSimpleHeader)) -> Tuple[RTCPPacket, int]:
        
        paylaod_size : int
        packet : (RTCPSRPacket | RTCPRRPacket | RTCPBYEPacket | RTCPSDESPacket | RTCPAPPPacket)
        if header.payload_type == RTPPayloadTypeEnum.RTCP_APP.value:
            
            packet, paylaod_size = RTCPParser.parse_rtcp_app_packet(raw_payload)
            
        elif header.payload_type == RTPPayloadTypeEnum.RTCP_BYE.value: 
            
            packet, paylaod_size = RTCPParser.parse_rtcp_bye_packet(raw_payload, header)
            
        elif header.payload_type == RTPPayloadTypeEnum.RTCP_RR.value: 
            
            packet, paylaod_size = RTCPParser.parse_rtcp_rr_packet(raw_payload, header)
            
        elif header.payload_type == RTPPayloadTypeEnum.RTCP_SDES.value: 
            
            packet, paylaod_size = RTCPParser.parse_rtcp_sdes_packet(raw_payload, header)
            
        elif header.payload_type == RTPPayloadTypeEnum.RTCP_SR.value: 
            
            packet, paylaod_size = RTCPParser.parse_rtcp_sr_packet(raw_payload, header)
        else:
            raise ValueError("Error parsing RTCP Packet, ", header.payload_type, " is not a RTCP Payload type")
        
        rtcp_packet = RTCPPacket()
        packet.header = header
        rtcp_packet.packet = packet
        
        return (rtcp_packet, paylaod_size)
    
    @staticmethod
    def parse_rtcp_bye_packet(raw_payload: bytearray, header: RTCPSimpleHeader) -> Tuple[RTCPBYEPacket, int]:

        packet = RTCPBYEPacket()
        paylaod_size: int
        packet.sources = [0] * header.block_count
        
        if len(raw_payload) >= header.block_count * SSRC_SIZE:
            
            if header.block_count > 0:
                
                for source_num in range(header.block_count):
                    
                    packet.sources[source_num] = int.from_bytes(raw_payload[source_num * SSRC_SIZE: (source_num + 1) * SSRC_SIZE])
                    
            paylaod_size = header.block_count * SSRC_SIZE
            
            if len(raw_payload) > header.block_count * SSRC_SIZE:
                
                packet.reason = RTCPBYEReason()
                packet.reason.length = int.from_bytes(raw_payload[header.block_count * SSRC_SIZE: header.block_count * SSRC_SIZE + 1])
                packet.reason.reason = raw_payload[header.block_count * SSRC_SIZE + 1: header.block_count * SSRC_SIZE + 1 + packet.reason.length].decode()
                # reason migth be padded
                paylaod_size = header.block_count * SSRC_SIZE + 1 + packet.reason.length
                while paylaod_size < len(raw_payload) and raw_payload[paylaod_size] == 0 :
                    paylaod_size += 1
        
        else:
            
            raise ValueError("RTCP BYE Packet was too short for ", header.block_count, " sources. Expecting at least ",
                             header.block_count * SSRC_SIZE, " octets but was ", len(raw_payload))
            
        return packet, paylaod_size
    
    @staticmethod
    def parse_rtcp_app_packet(raw_payload: bytearray) -> Tuple[RTCPAPPPacket, int]:
        
        packet = RTCPAPPPacket()
        payload_size : int
        
        if len(raw_payload) >= 4:
            
            packet.name = raw_payload[0:4].decode()
            packet.data, payload_size = RTCPParser.parse_rtcp_app_data(raw_payload[4:])
            
        else:
            
            raise ValueError("RTCP APP Packet was too small to contain name")
        
        return packet, payload_size + 4
    
    @staticmethod
    def parse_rtcp_app_data(raw_payload: bytearray) -> Tuple[bytearray, int]:
        
        # !!! Override this method to parse app specific data
        # return the number of octets consumed
        # this payload contains the APP name 4 first octets
        
        return raw_payload, len(raw_payload)
    

    @staticmethod
    def parse_rtcp_sdes_packet(raw_payload: bytearray, header: RTCPSimpleHeader) -> Tuple[RTCPSDESPacket, int]:

        packet = RTCPSDESPacket()
        packet.chuncks = [RTCPSDEChunk() for _ in range(header.block_count)]
        start_of_chunck = 0
        start_of_item = 0
        for chunck_num in range(header.block_count):

            if len(raw_payload) >= start_of_chunck + SSRC_SIZE:
                
                packet.chuncks[chunck_num].source = int.from_bytes(raw_payload[start_of_chunck: start_of_chunck + SSRC_SIZE])
                packet.chuncks[chunck_num].sdes_items = []
                start_of_item = start_of_chunck + SSRC_SIZE
                next_item_type = raw_payload[start_of_item]
                
                while next_item_type != 0:

                    # end of sdes item list is marked by null octets
                    start_of_item, next_item_type = RTCPParser.parse_rtcp_sdes_item(raw_payload, next_item_type, start_of_item, packet.chuncks[chunck_num])
                    
                # we now wait until next not null octet
                while start_of_item < len(raw_payload) and raw_payload[start_of_item] == 0:
                    
                    start_of_item += 1
                
                # ssrc may start with zeros bytes
                if start_of_item % 4 != 0:
                    start_of_item -= start_of_item % 4
                    
                start_of_chunck = start_of_item

            else:
                
                raise ValueError("RTCP SDES Chunck was too small to parse source")

        return packet, start_of_item
                
    @staticmethod
    def parse_rtcp_sdes_item(raw_payload: bytearray, next_item_type: int, start_of_item: int, chunck: RTCPSDEChunk) -> Tuple[int,int]:
        
        sdes_item = RTCPGenericItem()
        sdes_item.sdes_key = RTCPItemEnum._value2member_map_.get(next_item_type, None)
        
        if sdes_item.sdes_key is not None:
            
            sdes_item.length = raw_payload[start_of_item + 1]
            
            if len(raw_payload) >= start_of_item + 2 + sdes_item.length:
                
                sdes_item.sdes_value = raw_payload[start_of_item + 2: start_of_item + 2 + sdes_item.length].decode()
                
            else:
                
                raise ValueError("RTCP SDES Packet was too small to parse value of length ", sdes_item.length)
        else:
            
            raise KeyError("Unknown RTCP SDES Item with identifier ", next_item_type)
        
        chunck.sdes_items.append(sdes_item)
        
        return start_of_item + 2 + sdes_item.length, raw_payload[start_of_item + 2 + sdes_item.length]
        
    
    @staticmethod
    def parse_rtcp_sr_packet(raw_payload: bytearray, header: RTCPHeader) -> Tuple[RTCPSRPacket, int]:
        
        packet = RTCPSRPacket()
        packet.sender_info = RTCPSRSenderInfo()
        
        if len(raw_payload) >= SENDER_INFO_SIZE + header.block_count * REPORT_BLOCK_SIZE:
            
            packet.sender_info.ntp_timestamp = int.from_bytes(raw_payload[:8])
            packet.sender_info.rtp_timestamp = int.from_bytes(raw_payload[8:12])
            packet.sender_info.sender_packet_count = int.from_bytes(raw_payload[12:16])
            packet.sender_info.sender_octet_count = int.from_bytes(raw_payload[16:SENDER_INFO_SIZE])
            report_data = raw_payload[SENDER_INFO_SIZE: SENDER_INFO_SIZE + header.block_count * REPORT_BLOCK_SIZE]
            packet.profil_specific_data, extra_length = RTCPParser.rtcp_extract_sr_profile_specific_data(raw_payload[SENDER_INFO_SIZE + header.block_count * REPORT_BLOCK_SIZE:])
            packet.reports = RTCPParser.parse_rtcp_reports(report_data, header.block_count)
            
        else:
            
            raise ValueError("RTCP Sender report packet was too small to parse ", header.block_count, "reports")
        
        return packet, SENDER_INFO_SIZE + header.block_count * REPORT_BLOCK_SIZE + extra_length
    
    @staticmethod
    def parse_rtcp_reports(report_data: bytearray, block_count: int) -> list[RTCPReportBlock]:
        
        reports = [RTCPReportBlock() for _ in range(block_count)]
        
        for report_num in range(block_count):
            
            reports[report_num].ssrc = int.from_bytes(report_data[report_num * REPORT_BLOCK_SIZE: report_num * REPORT_BLOCK_SIZE + 4])
            reports[report_num].fraction_lost = int.from_bytes(report_data[report_num * REPORT_BLOCK_SIZE + 4 : report_num * REPORT_BLOCK_SIZE + 5])
            reports[report_num].cumul_packet_lost = int.from_bytes(report_data[report_num * REPORT_BLOCK_SIZE + 5: report_num * REPORT_BLOCK_SIZE + 8])
            reports[report_num].ext_highest_seq_num_received = int.from_bytes(report_data[report_num * REPORT_BLOCK_SIZE + 8: report_num * REPORT_BLOCK_SIZE + 12])
            reports[report_num].interarrival_jitter = int.from_bytes(report_data[report_num * REPORT_BLOCK_SIZE + 12: report_num * REPORT_BLOCK_SIZE + 16])
            reports[report_num].last_sr_timestamp = int.from_bytes(report_data[report_num * REPORT_BLOCK_SIZE + 16: report_num * REPORT_BLOCK_SIZE + 20])
            reports[report_num].delay_last_sr = int.from_bytes(report_data[report_num * REPORT_BLOCK_SIZE + 20: report_num * REPORT_BLOCK_SIZE + 24])
            
        return reports
    
    @staticmethod
    def parse_rtcp_rr_packet(raw_payload: bytearray, header: RTCPHeader) -> Tuple[RTCPRRPacket, int]:
        
        packet = RTCPRRPacket()
        
        if len(raw_payload) >= header.block_count * REPORT_BLOCK_SIZE:
            
            report_data = raw_payload[: header.block_count * REPORT_BLOCK_SIZE]
            packet.profil_specific_data, extra_length = RTCPParser.rtcp_extract_rr_profile_specific_data(raw_payload[header.block_count * REPORT_BLOCK_SIZE:])
            packet.reports = RTCPParser.parse_rtcp_reports(report_data, header.block_count)
            
        else:
            
            raise ValueError("RTCP Receiver report was too small to parse ", header.block_count," reports")
        
        return packet, header.block_count * REPORT_BLOCK_SIZE + extra_length
    
    @staticmethod
    def rtcp_extract_rr_profile_specific_data(data: bytearray) -> Tuple[bytearray, int]:
    
        # !!! Override to implement profile specific data
        
        return bytearray(), 0
    
    @staticmethod
    def rtcp_extract_sr_profile_specific_data(data: bytearray) -> Tuple[bytearray, int]:
    
        # !!! Override to implement profile specific data
        
        return bytearray(), 0