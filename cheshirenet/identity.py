"""
   Operations with cheshirenet identity
"""
import Image
import stepic
from ctypescrypt import pbkdf2,cipher,eckey

class Identity:
	"""
		Represents cheshirenet identity
	"""
	LEN_ENCINFO=8+32+16+16+32
	def __init__(self,filename,password):
		"""
			Loads cheshirenet identity from the steganographic file
			if filename doesn't contain appropreate steganographic
			block, creates empty identity to create using create
			method
		"""
		self.userpic=Image.open("filename")
		w,h=self.userpic.size
		if w<50 or h<50:
			raise ValueError("image to small for userpic")
		self.nickname=None
		try:
			data=stepic.decode(self.userpic)
		except Exception:
			return
		if len(data)!=self.LEN_ENCINFO:
			return
		self.salt=data[0:8]
		self.key=pbkdf2.PBKDF2(self.salt,password,2000,48)
		iv=self.key[32:48]
		key=self.key[0:32]
		c=cipher.new("AES-256-CFB",key,encrypt=False,iv=iv)
		deciphered=c.update(data[8:])
		deciphered+=c.finish()
		self.pkey=eckey.Eckey(deciphered[0:32]
		self.nf_name=UUID(bytes=deciphered[32:48]
		self.nf_iv=deciphered[48:64]
		self.nf_key=deciphered[64:96]

	@staticmethod
	def create(filename,password):
		"""
			Generates new cheshirenet identity, attaching given image
			to it.
		"""
		ident=Identity(filename,password)
		gen_data=rand.bytes(104,True)
		ident.salt=gen_data[0:8]
		ident.key=pbkdf2.PBKDF2(ident.salt,password,2000,48)
		ident.pkey=eckey.Eckey(gen_data[8:40])
		ident.nf_name=UUID(bytes=gen_data[40:56])
		ident.nf_iv=deciphered[56:72]
		ident.nf_key=deciphered[72:104]
		return ident

	
	def save(self,new_filename):
		"""
			Stores generated identity in the picture file
		"""
		to_encrypt=self.pkey.getprivbin+self.nf_name.bytes()+self.nf_iv+self.nf_key()
		c=cipher.new("AES-256-CFB",self.key[0:32],encrypt=True,iv=self.key[32:48]
		data=self.salt+c.update(to_encrypt)+c.finish()
		stepic.encode_inplace(self.userpic,data)
		f=open(new_filename,"wb")
		self.userpic.save(f,self.userpic.format)
		f.close

	def userpic(self):
		"""
			Returns userpic image with steganographic information
			cleared up.
		"""
		data=rand.pseudo_bytes(104)
		stepic.encode_inplace(self.userpic,data)
		return self.userpic.tostring(encoder_name=self.userpic.format)

	def nickname(self):
		"""
			Returns nickname of the user
		"""
		namegen.mkname(b16encode(self.pubkey_hash))
	def pubkey_hash():
		"""
			Returns SHA-256 hash of the pubkey
		"""
		d=digest.new("SHA-256")
		d.update(self.pubkey())
		return d.digest()
	
	def pubkey():
		"""
			Returns pubkey in the DER format
		"""
		return self.pkey.exportpub(format="DER")
	def sign(data):
		"""
			Returns signature for given data.
		"""
	def net_frag():
		"""
			Returns name (UUID) of the network fragment file
		"""
		return self.nf_name
	def cipher(encrypt=True):
		"""
			Returns cipher object to encrypt/decrypt network fragment
			file
		"""
		return cipher.new('AES-256-CFB',self.nf_key,encrypt=encrypt,iv=self.nf_iv)

