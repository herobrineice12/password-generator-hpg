from script.ENG_US.PasswordGen import Password
from script.Action import ask, showPassword, displayHash

def main(language):
	data_package = Password.askInstance()
	showPassword(data_package)
	if language:
		print(f"This password has {len(data_package[0])} characters\n")
	else:
		print(f"Essa senha tem {len(data_package[0])} caracteres")

	if data_package[1] != None and language:
		output = ask("Do you want to display the secret hash? (0,1): ")
	elif data_package[1] != None and not language:
		output = ask("Você quer que o script mostre o hash gerado? (0,1): ")
	displayHash(output, data_package)


if __name__ == main:
	main(False)