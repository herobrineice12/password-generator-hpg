import pyperclip
from ..SelectLanguage import language

def showPassword(data_package):
    print(f"\n{data_package[0]}")
    pyperclip.copy(data_package[0])

def displayHash(output, data_package):
    if output:
        print(f"{data_package[1]}")

def ask(message: str) -> bool:
    choice = [0,1]
    while True:
        try:
            variable = int(input(message))
            if variable in choice and variable == 0:
                return False
            elif variable in choice and variable == 1:
                return True
            elif variable == -1:
                exit()    
            break

        except Exception:
            print("Please, input the available options")