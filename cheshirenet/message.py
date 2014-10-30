"""
handles cheshirenet TLV message format

"""
class algs:
	"""
	Set of constants that name cheshirenet algorithms
	"""
	DIGEST="sha256"
	SIGN="ec"
	CURVE="secp256k1"
	CIPHER="aes-256-ofb"

class tags:
	"""
	Set of constants which define format flags
	"""
	SIGNATURE=0x1E
	PUBLICKEY=0x1F
	# Pseudo-tag added by parse
	VERIFIED=0x101

def __constructed(tag):
	"""
	Checks if given tag has constructed encoding 
	and should be parsed recursively
	"""
	return (tag & 0x20) !=0

def __length(buf,offset):
	"""
	Parses a length from the buffer starting and given offset
	returns pair (offset_of_data,length_of_data)
	"""
	if len(buf)<offset+2:
		raise ValueError("Corrupted message")
	n=ord(buf[offset])
	if n<128:
		return (offset+1,n)
	l=0
	end=offset+(n&0x7f)+1
	if len(buf)<end:
		raise ValueError("Corrupted message")
	for m in list(buf[offset+1:end]):
		l=(l<<8) | ord(m)
	return (end,l)

def __pack(tag,data):
	""" 
	Packs byte string into TLV structure with given tag
	"""
	l=len(data)
	s=chr(tag)
	if l<128:
		s+=chr(l)
	else:
		ll=""
		while l>0:
			ll=chr(l & 0xff)
			l>>=8
		s+=chr(0x80 | len(ll))+ll
	return s+data


def __verify(buf,signed_len,signature,key):
	"""
	Verifies signature under given data block
	"""
	key=pkey.PKey(pubkey=key,format="DER")
	h=digest.new(algs.DIGEST)
	h.update(buf,signed_len)
	return key.verify(h.digest())

def __sign(buf,key):
	"""
	Computes signature under given data block and appends it to
	block
	"""
	h=digest.new(algs.DIGEST)
	h.update(buf)
	return buf+__pack(tags.SIGNATURE,key.sign(h.digest()))+__pack(tags.PUBKEY,key.exportpub(format="DER"))

def parse(message,verify=True):
	"""
	Parses sequence of TLV structures into 
	"""
	d={}
	offset=0
	signedsize=None
	while offset<len(message):
		tag=ord(message[offset])
		start,len=__length(message,offset)
		if tag == tags.SIGNATURE:
			if signedsize is None:
				signedsize=offset
			else:
				raise ValueError("Duplicated signature")
		offset=start+length
		if len(message)<offset:
			raise ValueError("CorruptedMessage")
		data=message[start,offset]
		if __constructed(tag):
			data=parse(data,verify=verify)
		if tag in d:
			if isinstance(d,list):
				d[tag].append(data)
			else:
				d[tag]=[d.tag,data]
		else:
			d[tag]=data
	if verify and not signedsize is None:
		if not tags.PUBLICKEY in d:
			raise ValueError("CorruptedMessage: No signing key")
		d[tags.VERIFIED]=__verify(message,signedlen,d[tags.SIGNATURE],
			d[tags.PUBLICKEY])
	return d

def __serialize_item(tag,data,key,tosign):
	if tag >= 256:
		# Ignore pseudo-tag such as VERIFIED
		return ""
	if isinstanse(data,dict):
		data=serialize(t,data,key,tosign)
		if key is not None and t in tosign:
			data=__sign(data,key)
		return __pack(tag,data)
	else:
		return __pack(tag,data)
def serialize(tag,d,key=None,tosign=[]):
	"""
	Serializes message represented as nested dictionary into
	TLV structure with given tag.

	Signs it if necessary

	@param tag - tag for outer level TLV
	@param d - nested dictionary.
	@param key - secret key to sign message with
	@param tosign - list of tags which should be signed
	"""
	s=""
	for t in d:
		if isinstance(d[t],list):
			for item in d[t]:
				s+=__serialize_item(t,item,key,tosign)
		else:
			s+=__serialize_item(t,d[t],key,tosign)
	return __pack(tag,s)			
	
