import hashlib

class EncryptionHandler():
    # Salt for hash
    salt = "saltedbeefsteak"
    
    def createPasswordHash(self, password):
        # Generate password hash with salt
        password_hash = hashlib.sha224(password + EncryptionHandler.salt).hexdigest()

        return password_hash
        
    def createWebServiceKey(self, password_hash):
        # Generate the web service key with password hash and salt
        key = hashlib.sha224(password_hash + EncryptionHandler.salt).hexdigest()
        return key