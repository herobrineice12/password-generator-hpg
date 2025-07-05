from pyperclip import copy

def showPassword(data_package):
    print(f"\n{data_package[0]}")
    try:
        copy(data_package[0])
    except Exception as e:
        print(f"Erro: {e}")

def displayHash(output, data_package):
    if output:
        print(f"{data_package[1]}")

def ask(message: str) -> bool:
    choice = ['0','1']
    while True:
        try:
            variable = input(message)
            if variable == "-1":
                print("\nEnding the program...")
                exit(0)
            elif variable in choice:
                return variable == '1' 
            raise ValueError

        except Exception:
            print("Please, input a available options")

def intInput(message: str) -> int:
    MIN_LIMIT = -1
    MAX_LIMIT = 256

    while True:
        try:
            variable = int(input(message))
            if variable == -1:
                exit(0)

            if variable > MIN_LIMIT and variable <= MAX_LIMIT:
                return variable
            elif variable < MIN_LIMIT and variable > -MAX_LIMIT:
                return abs(variable)
            else:
                raise ValueError

        except Exception:
            print(f"Please, input a available option ({MIN_LIMIT} to finish the program, 0 for no limit and max of {MAX_LIMIT})")