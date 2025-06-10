import base64, hashlib, hmac, secrets
from argon2.low_level import hash_secret_raw, Type
from getpass import getpass
from .Action import ask

class Password:

	TRUNCATE_PADDING = 4

	def __init__(self, context: str, key1: str, key2: str, key3: str, master_key: str):
		self.context = context
		self.key1 = key1
		self.key2 = key2
		self.key3 = key3
		self.master_key = master_key

	@staticmethod
	def askInstance():
		data = [None] * 2

		print("Safe mode determines if the inputs used in the application will be show on the console")
		safe_mode = ask("Safe mode? (0,1): ")
		lock = int(input("Do you want to limit output length? (Nothing or 0 for no lock): "))
		hash = ask("Do you want to generate a hash for the master key? (0,1): ")
		base_permission = ask("Do you want a base85 password and the service supports it? (0,1): ")

		lock = None if lock in ['', 0] else lock

		if hash:
			secret_key = Password.hashGen(safe_mode)
			Shell = Password("","","","",secret_key)
			data[1] = secret_key
		else:
			Shell = Password("","","","","")

		if not safe_mode:
			print("Its important to keep the key, context and master key below a secret or private for more security")

		attributes = Shell.askInfo(safe_mode, hash)
		password = Shell.passwordGen(lock, attributes, base_permission)
		data[0] = password

		return data
	
	@staticmethod
	def hashGen(safe_mode):
		input_method = getpass if safe_mode else input
		message = input_method("Write the message you want to be used as: ")
		secret_key = secrets.token_bytes(32)

		encoded_hash = hmac.new(key = secret_key, msg = message.encode('utf-8'), digestmod = "sha256").digest()
		generated_hash = base64.b64encode(encoded_hash)

		return generated_hash.decode('utf-8')

	def askInfo(self, safe_mode, hash):
		seeds = [self.context, self.key1, self.key2, self.key3,self.master_key]
		attribute_names = ["context","key1","key2","key3","master key"]
		input_method = getpass if safe_mode else input

		for i in range(5):
			if hash and i == 4:
				continue
			seeds[i] = input_method(f"Set a value for {attribute_names[i]}: ")

		return seeds
    
	def passwordGen(self, outputSize, seeds, base_permission):
		blake_mixer = hashlib.blake2b(key = seeds[1].encode('utf-8'), digest_size = 64)
		
		blake_mixer.update(f"{seeds[2]}:{seeds[3]}".encode('utf-8'))
		supersalt = blake_mixer.digest()

		hash_bytes = hash_secret_raw(
			secret = seeds[4].encode('utf-8'), salt = supersalt, time_cost = 20,
			memory_cost = 256042, parallelism = 2, hash_len = 64, type = Type.ID)

		if base_permission:
			final_encoded = base64.b85encode(hash_bytes).decode('utf-8')
		else:
			final_encoded = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')

		processed_password = Password.intertwine(final_encoded)
		return processed_password[:outputSize] if outputSize else processed_password
	
	@staticmethod
	def intertwine(password):
		sha512_hash = hashlib.sha512(password[::-1].encode('utf-8')).digest()
		encoded_hash = base64.urlsafe_b64encode(sha512_hash).decode('utf-8')

		intertwined = ''.join(a + b for a, b in zip(encoded_hash, password))

		# The code return a passowrd with 4 '=' equal signs at the end,
		# the "-4" operation is to get rid of that
		return intertwined[:-Password.TRUNCATE_PADDING]