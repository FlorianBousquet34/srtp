## Real-time Transport Protocol and Secure Real-time Transport Protocol

# An Implementation of the real-time transfert protocol and it's control packets

This project is an implementation in python of the secure real-time transfert protocol (SRTP)  
described in RFC 3550 and the real-time transfert protocol (RTP) described in RFC 3711.  
It also includes the control packets for both implementations RTCP (resp SRTCP) and the  
monitoring of the transfert session.

## Install

# first install the required packages

```
pip install -r requirements.txt
```

## How to use

# To create a new RTP Session

First create a session profile RTPSessionContext with the estimated packet size (in octets) in the session  
and the bandwith. Other parameters can also be twecked.  
Then create a RTPSession with this profile.  
Then create a RTPParticipant with a random ssrc and the SDES info (at least a CNAME for validation).  
Finally, the function join_session from RTPParticipant can be used to join the session

# To join an active RTP Session

To join an active session, the data corresponding to this session is needed.  
Then a RTPPaticipant can be created and the method join_session can be used.

# To create a new SRTP Session

It is almost the same as a RTP Session, create a SRTPCryptoContext to indicate the extra informations  
that are not required with simple RTP.  
Then create a SRTP Session and a RTPParticipant.  
Finally the same method join session can be used.
