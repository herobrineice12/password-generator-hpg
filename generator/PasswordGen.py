import base64, hashlib, hmac, secrets
from argon2.low_level import hash_secret_raw, Type
from getpass import getpass
from .Action import ask, intInput
from .PrimeGen import PrimeGen

class Password:
	def __init__(self, context: str = None, key1: str = None, key2: str = None, key3: str = None, master_key: str = None):
		self.context = context
		self.key1 = key1
		self.key2 = key2
		self.key3 = key3
		self.master_key = master_key

	@staticmethod
	def askInstance(json) -> list:
		global dialog
		global safe_mode

		dialog = json
		data: list = [None] * 2

		print(dialog["safe_mode_instruction"])
		safe_mode = ask(dialog["safe_mode_input"])
		lock: bool = intInput(dialog["lock_input"])
		hash: bool = ask(dialog["generate_message_input"])
		base_permission: bool = ask(dialog["base_permission_input"])

		lock: int = 255 if lock in ['', 0] else lock

		if hash:
			secret_key = Password.hashGen()
			Shell = Password(master_key=secret_key)
			data[1] = secret_key
		else:
			Shell = Password()

		if not safe_mode:
			print(dialog["safe_mode_warning"])

		attributes = Shell.askInfo()
		password = Shell.passwordGen(attributes, base_permission, lock)
		data[0] = password

		return data
	
	@staticmethod
	def hashGen() -> str:
		input_method = getpass if safe_mode else input

		message: str = input_method(dialog["hash_message_input"])
		print(dialog["generate_hash_instruction"])
		
		secret_key: str = intInput(dialog["generate_rounds_input"], -1, 32)
		print(dialog["generate_hash_calculated"] + str(2**secret_key))

		key_bits: int = secrets.randbits(secret_key)
		key_hash: str = PrimeGen.primeCounter(key_bits)

		encoded_hash = hmac.new(key = key_hash.encode('utf-8'), msg = message.encode('utf-8'), digestmod = "sha256").digest()
		generated_hash: bytes = base64.b64encode(encoded_hash)

		return generated_hash.decode('utf-8')

	def askInfo(self) -> list:
		seeds: list = [self.context, self.key1, self.key2, self.key3,self.master_key]
		attribute_names: list = [dialog["context"],dialog["key1"],dialog["key2"],dialog["key3"],dialog["master_key"]]
		input_method = getpass if safe_mode else input

		for i in range(5):
			if seeds[i] == None:
				seeds[i] = input_method(dialog["value_set_input"] + attribute_names[i] + ": ")

		return seeds
    
	def passwordGen(self, seeds, base_permission, output_size) -> str:
		blake_mixer = hashlib.blake2b(key = f"{seeds[1]}:{seeds[0]}".encode('utf-8'), digest_size = 64)
		
		blake_mixer.update(f"{seeds[2]}:{seeds[3]}".encode('utf-8'))
		supersalt: bytes = blake_mixer.digest()

		hash_bytes: bytes = hash_secret_raw(
			secret = seeds[4].encode('utf-8'), salt = supersalt, time_cost = 20,
			memory_cost = 256042, parallelism = 2, hash_len = 128, type = Type.ID)

		if base_permission: final_encoded: str = base64.b85encode(hash_bytes).decode('utf-8')
		else: final_encoded: str = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')

		processed_password = Password.intertwine(final_encoded, base_permission)
		return processed_password[:output_size] if output_size else processed_password
	
	@staticmethod
	def intertwine(password, base_permition, loop: bool = False) -> str:
		sha512_hash: bytes = hashlib.sha512(password[::-1].encode('utf-8')).digest()
		encoded_hash: str = base64.urlsafe_b64encode(sha512_hash).decode('utf-8')

		intertwined: str = ''.join(a + b for a, b in zip(encoded_hash, password))

		if loop:
			return intertwined

		if base_permition:
			expansion: str = base64.b85encode(hashlib.blake2b(intertwined.encode(),digest_size = 64).digest()).decode('utf-8')			
		else:
			expansion: str = base64.b64encode(hashlib.blake2b(password.encode(),digest_size = 64).digest()).decode('utf-8')
		
		expansion = Password.intertwine(expansion, True, True)

		intertwined = ''.join(a + b for a, b in zip(expansion, intertwined))
		return intertwined.strip('=')
