import generator.Action as Action
import os, json, sys
from generator.PasswordGen import Password

def main(dialog) -> None:
	data_package: list = Password.askInstance(dialog)

	Action.showPassword(data_package)
	print(dialog["password_length"] + str(len(data_package[0])) + "\n")

	if data_package[1] != None:
		output: bool = Action.ask(dialog["hash_show"] + "\n")
		if output: print("\n" + data_package[1] + "\n")

if __name__ == "__main__":
	try:
		language_mode: bool = input("(1) English\n(2) Português\n-> ")
		if language_mode == '1': file_name = "eng.json"
		elif language_mode == '2': file_name = "pt-br.json"
		else: raise ValueError
		
		if getattr(sys,'frozen',False): base_path = sys._MEIPASS
		else: base_path: str = os.path.dirname(__file__)

		rel_path: str = os.path.join(base_path,"config",file_name)

		with open(rel_path,'r',encoding='utf-8') as file:
			dialog = json.load(file)
	except ValueError:
		print("Language selection failed, restart the script to try again")
		sys.exit(0)
	except FileNotFoundError:
		print("The file was not found")
		sys.exit(1)
	except Exception as e:
		print(f"Erro: {e}")
		sys.exit(1)

	while True:
		try:
			main(dialog)
		except KeyboardInterrupt:
			print("\nEnding the program...")
			sys.exit(0)
		except Exception as e:
			print(f"Erro: {e}")
			sys.exit(1)
