import config.Action as Action
import os, json
from generator.PasswordGen import Password

def main(dialog):
	data_package = Password.askInstance(dialog)

	Action.showPassword(data_package)
	print(dialog["password_length"] + str(len(data_package[0])) + "\n")

	if data_package[1] != None:
		output = Action.ask(dialog["hash_show"] + "\n")
		if output: print("\n" + data_package[1])

if __name__ == "__main__":
	loop = True

	try:
		language_mode = input("(1) English\n(2) Português\n-> ")
		if language_mode == '1': rel_path = os.path.join("config","eng.json")
		elif language_mode == '2' : rel_path = os.path.join("config","pt-br.json")
		else: raise ValueError

		with open(rel_path,'r',encoding='utf-8') as file:
			dialog = json.load(file)

	except ValueError:
		print("Language selection failed, restart the script to try again")
		exit(0)
	except Exception as e:
		print(f"Erro: {e}")
		exit(1)

	while loop:
		try:
			main(dialog)
		except KeyboardInterrupt:
			print("\nEnding the program...")
			exit(0)
		except Exception as e:
			print(f"Erro: {e}")
			exit(1)
