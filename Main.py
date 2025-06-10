import pyperclip
from script.PasswordGen import Password
from script.Action import ask

if __name__ == "__main__":
	data_package = Password.askInstance()
	print(f"\n{data_package[0]}")
	pyperclip.copy(data_package[0])
	print(f"This password has {len(data_package[0])} characters\n")
	if len(data_package) == 2:
		output = ask("Do you want to display the secret hash? (0,1): ")
		if output:
			print(f"{data_package[1]}")