from src.main.model.rtcp.RTCPConsts import REPORT_BLOCK_SIZE


class RTCPReportBlock:
    
    def to_bytes(self) -> bytearray:
        
        raw_data = bytearray(REPORT_BLOCK_SIZE)
        raw_data[:4] = self.ssrc.to_bytes(4)
        raw_data[4] = self.fraction_lost
        raw_data[5:8] = self.cumul_packet_lost.to_bytes(3)
        raw_data[8:12] = self.ext_highest_seq_num_received.to_bytes(4)
        raw_data[12:16] = self.interarrival_jitter.to_bytes(4)
        raw_data[16:20] = self.last_sr_timestamp.to_bytes(4)
        raw_data[20:24] = self.delay_last_sr.to_bytes(4)
        
        return raw_data
    
    # The The SSRC identifier of the source to which the information in this
    # reception report block pertains 32 bits
    ssrc: int
    
    # Lost fraction 8 bits
    # The fraction of RTP data packets from source SSRC_n lost since the
    # previous SR or RR packet was sent, expressed as a fixed point
    # number with the binary point at the left edge of the field.  (That
    # is equivalent to taking the integer part after multiplying the
    # loss fraction by 256.)  This fraction is defined to be the number
    # of packets lost divided by the number of packets expected
    # min is 0 (if neg because of duplicates)
    fraction_lost: int
    
    # The cumulative number of packet lost relative to the block source
    # sing beginning 24 bits
    cumul_packet_lost : int
    
    # The low 16 bits contain the highest sequence number received in an
    # RTP data packet from source SSRC_n, and the most significant 16
    # bits extend that sequence number with the corresponding count of
    # sequence number cycles (32 bits total)
    ext_highest_seq_num_received: int
    
    # interarrival jitter 32 btis
    # impl https://datatracker.ietf.org/doc/html/rfc3550#appendix-A.8
    interarrival_jitter : int
    
    # The middle 32 bits out of 64 in the NTP timestamp received in last
    # SR from source ssrc
    last_sr_timestamp: int
    
    # Delay since source ssrc last SR report
    # 0 if none received
    # 32 bits 
    # 1 bit => 1/65536 sec
    delay_last_sr: int