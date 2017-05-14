from Crypto.Cipher import AES
from Crypto import Random

# AES Cipher implementation
class AESCipher:
    #Block size
    blocksize = 16
    
    # Padding 
    def pad(self, s):
        return (s +  (self.blocksize - len(s) % self.blocksize) * chr(self.blocksize - len(s) % self.blocksize))
    
    # unpadding/removing pad
    def unpad(self, s):
        return s[0:-ord(s[-1])]
    
    # default Constructor, it Requires hex encoded param as a key
    def __init__( self, key ): 
        self.key = key.decode("hex")
    
    # returns hex encoded encrypted value
    def encrypt( self, raw ): 
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size);
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return ( iv + cipher.encrypt( raw ) ).encode("hex")

    # requires hex encoded param to decrypt
    def decrypt( self, enc ): 
        enc = enc.decode("hex")
        iv = enc[:16]
        enc= enc[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return self.unpad(cipher.decrypt( enc))
 