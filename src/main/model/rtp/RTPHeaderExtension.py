class RTPHeaderExtension:
    
    # a 16 bits identifier giving the signification of the extension
    extensionImplemIdentifier: int
    
    # The length of the extention payload on 16 bits
    # (length of wordlist)
    length: int 
    
    # list of size length of 32 bits words
    wordList: list[str] 