from main.model.rtcp.RTCPCompoundPacket import RTCPCompoundPacket
from main.model.rtcp.RTCPHeader import RTCPHeader
from main.model.rtcp.RTCPPacket import RTCPPacket
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

REPORT_BLOCK_SIZE = 24
HEADER_SIZE = 8
SSRC_SIZE = 4
SENDER_INFO_SIZE = 20

class RTCPParser:
    
    @staticmethod
    def parse_rtcp_compound_packet(packet: RTCPCompoundPacket):
        
        if len(packet.raw_data) >= HEADER_SIZE:
            
            raw_header = packet.raw_data[:HEADER_SIZE]
            header : RTCPHeader = RTCPParser.parse_rtcp_header(raw_header)
        
            start_of_packet = HEADER_SIZE
            packet.packets = [None] * header.block_count
            
            for rtcp_packet_num in range(header.block_count):
            
                start_of_packet = RTCPParser.parse_rtcp_packet(packet, start_of_packet, rtcp_packet_num)
        
        else:
            raise ValueError("The RTCP Compound packet received is too small, header could not be parse." +
                             "*it can also be a packet without data")
        
        
    @staticmethod
    def parse_rtcp_packet(compound_packet: RTCPCompoundPacket, start_of_packet: int, rtcp_packet_num: int) -> int:
        
        if len(compound_packet.raw_data) >= start_of_packet + HEADER_SIZE:
            
            raw_header = compound_packet.raw_data[start_of_packet: start_of_packet + HEADER_SIZE]
            header : RTCPHeader = RTCPParser.parse_rtcp_header(raw_header)
            
            if len(compound_packet.raw_data) >= start_of_packet + HEADER_SIZE + header.length:
                
                raw_payload = compound_packet.raw_data[start_of_packet + HEADER_SIZE: start_of_packet + HEADER_SIZE + header.length]
                packet, payload_size = RTCPParser.parse_rtcp_payload(raw_payload, header)
                compound_packet.packets[rtcp_packet_num] = packet
                
            else:
                
                raise ValueError("The body of the RTCP Packet was smaller than the given length")
        else:
            
            raise ValueError("The RTCP Compound block was too small to read the header")
        
        return payload_size + HEADER_SIZE
    
    @staticmethod
    def parse_rtcp_header(raw_header: bytearray) -> RTCPHeader:
        
        header = RTCPHeader()
        header.version = int((raw_header >> 1) & 0b11)
        
        if header.version == 2:
            
            header.length = int(raw_header[2:4])
            header.padding = (raw_header >> 3) & 1 != 1
            header.block_count = int((raw_header >> 4 ) & 0b11111)
            header.payload_type = int((raw_header >> 10) & 0b1111111)
            header.ssrc = int(raw_header[4:4 + SSRC_SIZE])
            
        else:
            raise ValueError("The RTCP Compound packed was not well formated, It must contain 4 octets blocks")
        
        return header
    
    @staticmethod
    def parse_rtcp_payload(raw_payload: bytearray, header: RTCPHeader) -> (RTCPPacket, int):
        
        paylaod_size : int
        packet : RTCPPacket = None
        
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
            
        packet.packet.header = header
        
        return (packet, paylaod_size)
    
    @staticmethod
    def parse_rtcp_bye_packet(raw_payload: bytearray, header: RTCPHeader) -> (RTCPBYEPacket, int):
        # the first ssrc is in header for genericity purpose
        packet = RTCPBYEPacket()
        paylaod_size: int
        packet.sources = [None] * header.block_count
        payload_ssrc_count = header.block_count - 1
        
        if len(raw_payload) >= payload_ssrc_count * SSRC_SIZE:
            
            packet.sources[0] = header.ssrc
            
            if payload_ssrc_count > 0:
                
                for source_num in range(payload_ssrc_count):
                    
                    packet.sources[source_num + 1] = int(raw_payload[source_num * SSRC_SIZE: (source_num + 1) * SSRC_SIZE])
                    
            paylaod_size = payload_ssrc_count * SSRC_SIZE
            
            if len(raw_payload) > payload_ssrc_count * SSRC_SIZE:
                
                packet.reason = RTCPBYEReason()
                packet.reason.length = int(raw_payload[payload_ssrc_count * SSRC_SIZE: payload_ssrc_count * SSRC_SIZE + 1])
                packet.reason.reason = str(raw_payload[payload_ssrc_count * SSRC_SIZE + 1: payload_ssrc_count * SSRC_SIZE + 1 + packet.reason.length])
                paylaod_size = payload_ssrc_count * SSRC_SIZE + 1 + packet.reason.length
        
        else:
            
            raise ValueError("RTCP BYE Packet was too short for ", header.block_count, " sources. Expecting at least ",
                             header.block_count * SSRC_SIZE, " octets but was ", len(raw_payload))
            
        return packet, paylaod_size
    
    @staticmethod
    def parse_rtcp_app_packet(raw_payload: bytearray) -> RTCPAPPPacket:
        
        packet = RTCPAPPPacket()
        payload_size : int
        
        if len(raw_payload) >= 4:
            
            packet.name = str(raw_payload[0:4])
            packet.data, payload_size = RTCPParser.parse_rtcp_app_data(raw_payload)
            
        else:
            
            raise ValueError("RTCP APP Packet was too small to contain name")
        
        return packet, payload_size
    
    @staticmethod
    def parse_rtcp_app_data(raw_payload: bytearray):
        
        # !!! Override this method to parse app specific data
        # return the number of octets consumed
        # this payload contains the APP name 4 first octets
        
        return raw_payload, len(raw_payload)
    

    @staticmethod
    def parse_rtcp_sdes_packet(raw_payload: bytearray, header: RTCPHeader) -> RTCPSDESPacket:
        #The ssrc of the first chunck is in header.ssrc for generic purpose
        packet = RTCPSDESPacket()
        packet.chuncks = [None] * header.block_count
        full_raw_payload = int.to_bytes(header.ssrc) + raw_payload
        start_of_chunck = 0
        
        for chunck_num in range(header.block_count):
            
            if len(full_raw_payload) >= start_of_chunck + SSRC_SIZE:
                
                chunck = RTCPSDEChunk()
                chunck.source = int(full_raw_payload[start_of_chunck: start_of_chunck + SSRC_SIZE])
                chunck.sdes_items = []
                start_of_item = start_of_chunck + SSRC_SIZE
                next_item_type = full_raw_payload[start_of_item]
                
                while next_item_type != 0:
                    
                    # end of sdes item list is marked by null octets
                    start_of_item, next_item_type = RTCPParser.parse_rtcp_sdes_item(full_raw_payload, next_item_type, start_of_item, chunck)
                    
                # we now wait until next not null octet
                while full_raw_payload[start_of_item] == 0:
                    
                    start_of_item += 1
                    
                packet.chuncks[chunck_num] = chunck
            else:
                
                raise ValueError("RTCP SDES Chunck was too small to parse source")
            
        return packet
                
    @staticmethod
    def parse_rtcp_sdes_item(full_raw_payload: bytearray, next_item_type: int, start_of_item: int, chunck: RTCPSDEChunk):
        
        sdes_item = RTCPGenericItem()
        sdes_item.sdes_key = RTCPItemEnum._value2member_map_.get(next_item_type, None)
        
        if sdes_item.sdes_key is not None:
            
            sdes_item.length = full_raw_payload[start_of_item + 1]
            
            if len(full_raw_payload) >= start_of_item + 2 + sdes_item.length:
                
                sdes_item.sdes_value = str(full_raw_payload[start_of_item + 2: start_of_item + 2 + sdes_item.length])
                
            else:
                
                raise ValueError("RTCP SDES Packet was too small to parse value of length ", sdes_item.length)
        else:
            
            raise KeyError("Unknown RTCP SDES Item with identifier ", next_item_type)
        
        chunck.sdes_items.append(sdes_item)
        
        return start_of_item + 2 + sdes_item.length, full_raw_payload[start_of_item + 2 + sdes_item.length]
        
    
    @staticmethod
    def parse_rtcp_sr_packet(raw_payload: bytearray, header: RTCPHeader) -> RTCPSRPacket:
        
        packet = RTCPSRPacket()
        packet.sender_info = RTCPSRSenderInfo()
        
        if len(raw_payload) >= SENDER_INFO_SIZE + header.block_count * REPORT_BLOCK_SIZE:
            
            packet.sender_info.ntp_timestamp = int(raw_payload[:8])
            packet.sender_info.rtp_timestamp = int(raw_payload[8:12])
            packet.sender_info.sender_packet_count = int(raw_payload[12:16])
            packet.sender_info.sender_octet_count = int(raw_payload[16:SENDER_INFO_SIZE])
            report_data = raw_payload[SENDER_INFO_SIZE: SENDER_INFO_SIZE + header.block_count * REPORT_BLOCK_SIZE]
            packet.profil_specific_data = raw_payload[SENDER_INFO_SIZE + header.block_count * REPORT_BLOCK_SIZE:]
            packet.reports = RTCPParser.parse_rtcp_reports(report_data, header.block_count)
            
        else:
            
            raise ValueError("RTCP Sender report packet was too small to parse ", header.block_count, "reports")
        
        return packet
    
    @staticmethod
    def parse_rtcp_reports(report_data: bytearray, block_count: int) -> list[RTCPReportBlock]:
        
        reports = [None] * block_count
        
        for report_num in range(block_count):
            
            block = RTCPReportBlock()
            block.ssrc = int(report_data[report_num * REPORT_BLOCK_SIZE: report_num * REPORT_BLOCK_SIZE + 4])
            block.fraction_lost = int(report_data[report_num * REPORT_BLOCK_SIZE + 4 : report_num * REPORT_BLOCK_SIZE + 5])
            block.cumul_packet_lost = int(report_data[report_num * REPORT_BLOCK_SIZE + 5: report_num * REPORT_BLOCK_SIZE + 8])
            block.ext_highest_seq_num_received = int(report_data[report_num * REPORT_BLOCK_SIZE + 8: report_num * REPORT_BLOCK_SIZE + 12])
            block.interarrival_jitter = int(report_data[report_num * REPORT_BLOCK_SIZE + 12: report_num * REPORT_BLOCK_SIZE + 16])
            block.last_sr_timestamp = int(report_data[report_num * REPORT_BLOCK_SIZE + 16: report_num * REPORT_BLOCK_SIZE + 20])
            block.delay_last_sr = int(report_data[report_num * REPORT_BLOCK_SIZE + 20: report_num * REPORT_BLOCK_SIZE + 24])
            reports[report_num] = block
            
        return reports
    
    @staticmethod
    def parse_rtcp_rr_packet(raw_payload: bytearray, header: RTCPHeader) -> RTCPRRPacket:
        
        packet = RTCPRRPacket()
        
        if len(raw_payload) >= header.block_count * REPORT_BLOCK_SIZE:
            
            report_data = raw_payload[: header.block_count * REPORT_BLOCK_SIZE]
            packet.profil_specific_data = raw_payload[header.block_count * REPORT_BLOCK_SIZE:]
            packet.reports = RTCPParser.parse_rtcp_reports(report_data, header.block_count)
            
        else:
            
            raise ValueError("RTCP Receiver report was too small to parse ", header.block_count," reports")
        
        return packet