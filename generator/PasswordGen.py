import base64, hashlib, hmac, secrets
from argon2.low_level import hash_secret_raw, Type
from typing import Optional
from getpass import getpass
from Action import ask, intInput

class Password:
	def __init__(self, context: str, key1: str, key2: str, key3: str, master_key: str):
		self.context = context
		self.key1 = key1
		self.key2 = key2
		self.key3 = key3
		self.master_key = master_key

	@staticmethod
	def askInstance(json):
		global dialog
		dialog = json
		data = [None] * 2

		print(dialog["safe_mode_instruction"])
		safe_mode = ask(dialog["safe_mode_input"])
		lock = intInput(dialog["lock_input"])
		hash = ask(dialog["generate_message_input"])
		base_permission = ask(dialog["base_permission_input"])

		lock = 255 if lock in ['', 0] else lock

		if hash:
			secret_key = Password.hashGen(safe_mode)
			Shell = Password("","","","",secret_key)
			data[1] = secret_key
		else:
			Shell = Password("","","","","")

		if not safe_mode:
			print(dialog["safe_mode_warning"])

		attributes = Shell.askInfo(safe_mode, hash)
		password = Shell.passwordGen(attributes, base_permission, lock)
		data[0] = password

		return data
	
	@staticmethod
	def hashGen(safe_mode):
		input_method = getpass if safe_mode else input
		message = input_method(dialog["hash_message_input"])
		secret_key = secrets.token_bytes(32)

		encoded_hash = hmac.new(key = secret_key, msg = message.encode('utf-8'), digestmod = "sha256").digest()
		generated_hash = base64.b64encode(encoded_hash)

		return generated_hash.decode('utf-8')

	def askInfo(self, safe_mode, hash):
		seeds = [self.context, self.key1, self.key2, self.key3,self.master_key]
		attribute_names = [dialog["context"],dialog["key1"],dialog["key2"],dialog["key3"],dialog["master_key"]]
		input_method = getpass if safe_mode else input

		for i in range(5):
			if hash and i == 4:
				continue
			seeds[i] = input_method(dialog["value_set_input"] + attribute_names[i] + "...: ")

		return seeds
    
	def passwordGen(self, seeds, base_permission, output_size):
		blake_mixer = hashlib.blake2b(key = f"{seeds[1]}:{seeds[0]}".encode('utf-8'), digest_size = 64)
		
		blake_mixer.update(f"{seeds[2]}:{seeds[3]}".encode('utf-8'))
		supersalt = blake_mixer.digest()

		hash_bytes = hash_secret_raw(
			secret = seeds[4].encode('utf-8'), salt = supersalt, time_cost = 20,
			memory_cost = 256042, parallelism = 2, hash_len = 128, type = Type.ID)

		if base_permission:
			final_encoded = base64.b85encode(hash_bytes).decode('utf-8')
		else:
			final_encoded = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')

		processed_password = Password.intertwine(final_encoded, base_permission)
		return processed_password[:output_size] if output_size else processed_password
	
	@staticmethod
	def intertwine(password, base_permition, loop: Optional[bool] = False) -> str:
		sha512_hash = hashlib.sha512(password[::-1].encode('utf-8')).digest()
		encoded_hash = base64.urlsafe_b64encode(sha512_hash).decode('utf-8')

		intertwined = ''.join(a + b for a, b in zip(encoded_hash, password))

		if loop:
			return intertwined

		# if you dont use the base85, the code return a passowrd with 4 '=' equal signs at the end,
		# the "-4" operation is to get rid of that
		if base_permition:
			expansion = base64.b85encode(hashlib.blake2b(intertwined.encode(),digest_size = 64).digest()).decode('utf-8')			
			expansion = Password.intertwine(expansion, True, True)

			intertwined = ''.join(a + b for a, b in zip(expansion, intertwined))
			return intertwined
		else:
			expansion = base64.b64encode(hashlib.blake2b(password.encode(),digest_size = 64).digest()).decode('utf-8')
			expansion = Password.intertwine(expansion, True, True)

			intertwined = ''.join(a + b for a, b in zip(expansion, intertwined))
			return intertwined.strip('=')
