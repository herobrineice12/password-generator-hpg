import base64, hashlib, hmac, secrets
from argon2.low_level import hash_secret_raw, Type
from getpass import getpass
from typing import Optional
from ..Action import ask, intInput

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

		print("O modo seguro determina se o que estiver escrevendo apareça para você e terceiros no console")
		safe_mode = ask("Modo seguro? (0,1): ")
		lock = intInput("Gostaria de limitar o tamanho da senha? (Não digite ou envie 0 para sem limites): ")
		hash = ask("Gostaria de gerar um hash para a master key? (0,1): ")
		base_permission = ask("Você gostaria de usar base85 e sabe se o seu serviço suporta? (0,1): ")

		lock = 255 if lock in ['', 0] else lock

		if hash:
			secret_key = Password.hashGen(safe_mode)
			Shell = Password("","","","",secret_key)
			data[1] = secret_key
		else:
			Shell = Password("","","","","")

		if not safe_mode:
			print("É importante manter o contexto da chave, chaves e senha mestra privadas ou em segredo para maior segurança")

		attributes = Shell.askInfo(safe_mode, hash)
		password = Shell.passwordGen(attributes, base_permission, lock)
		data[0] = password

		return data
	
	@staticmethod
	def hashGen(safe_mode):
		input_method = getpass if safe_mode else input
		message = input_method("Escreva a mensagem que gostaria de utilizar para criar o hash: ")
		secret_key = secrets.token_bytes(64)

		encoded_hash = hmac.new(key = secret_key, msg = message.encode('utf-8'), digestmod = "sha3_256").digest()
		generated_hash = base64.b64encode(encoded_hash)

		return generated_hash.decode('utf-8')

	def askInfo(self, safe_mode, hash):
		seeds = [self.context, self.key1, self.key2, self.key3,self.master_key]
		attribute_names = ["contexto","chave 1","chave 2","chave 3","senha mestra"]
		input_method = getpass if safe_mode else input

		for i in range(5):
			if hash and i == 4:
				continue
			seeds[i] = input_method(f"Decida um valor para {attribute_names[i]}: ")

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
		sha512_hash = hashlib.sha3_512(password[::-1].encode('utf-8')).digest()
		encoded_hash = base64.urlsafe_b64encode(sha512_hash).decode('utf-8')

		intertwined = ''.join(a + b for a, b in zip(encoded_hash, password))

		if loop:
			return intertwined

		# Se não utilizar o base85, a sua senha retornará com pelo menos 4 sinais de '=' no final da senha,
		# o "-4" serve para se livrar disso
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