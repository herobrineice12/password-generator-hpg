from script import Action
from script.ENG_US import PasswordGen
from script.PT_BR import GeradorSenha

def main(language):
	data_package = GeradorSenha.Password.askInstance() if language == True else PasswordGen.Password.askInstance()

	Action.showPassword(data_package)
	if language:
		print(f"Essa senha tem {len(data_package[0])} caracteres")
	else:
		print(f"This password has {len(data_package[0])} characters\n")

	output = None
	if data_package[1] != None and Action.language:
		output = Action.ask("Você quer que o script mostre o hash gerado? (0,1): ")
	elif data_package[1] != None and not Action.language:
		output = Action.ask("Do you want to display the secret hash? (0,1): ")
	
	if output != None:
		Action.displayHash(output, data_package)

if __name__ == "__main__":
	loop = True

	while loop:
		try:
			language = Action.ask("English/Português? (0,1): ")
			main(language)

			if language:
				loop = Action.ask("Gostaria de gerar outra senha? (0,1): ")
			else:
				loop = Action.ask("Would you like to generate another password? (0,1): ")
		except KeyboardInterrupt:
			print("\nEnding the program...")
			exit(0)