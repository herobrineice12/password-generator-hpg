import Action
from generator.PasswordGen import Password
from config import json

def main(dialog):
	data_package = Password.askInstance(dialog)

	Action.showPassword(data_package)
	print(dialog["password_length"] + str(len(data_package[0])))

	if data_package[1] != None:
		output = Action.ask(dialog["hash_show"])
		if output:
			print(data_package[1])

if __name__ == "__main__":
	loop = True

	try:
		language_mode = input("(1) English\n(2) Português\n-> ")
		if language_mode == '1':
			path = "config/eng.json"
		elif language_mode == '2':
			path = "config/pt-br.json"
		else:
			raise ValueError

		dialog = json.load(path)
	except ValueError:
		print("Language selection failed, restart the script to try again")
		exit(0)

	while loop:
		try:
			main(dialog)
		except KeyboardInterrupt:
			print("\nEnding the program...")
			exit(0)
