from pyperclip import copy
import secrets, sys

def showPassword(data_package) -> None:
    print(f"\n{data_package[0]}\n")
    try:
        copy(data_package[0])
    except Exception as e:
        print(f"Erro: {e}")

def displayHash(output, data_package):
    if output:
        print(f"{data_package[1]}")

def ask(message: str, choice: list[str] = ['0','1']) -> bool:
    while True:
        try:
            variable = input(message)
            if variable == "-1":
                print("\nEnding the program...")
                sys.exit(0)
            elif variable in choice:
                return variable == '1' 
            raise ValueError

        except Exception:
            print("Please, input a available options")

def intInput(message: str, MIN_LIMIT: int = -1, MAX_LIMIT: int = 256) -> int:
    while True:
        try:
            variable = int(input(message))
            if variable == -1:
                sys.exit(0)

            if variable > MIN_LIMIT and variable <= MAX_LIMIT:
                return variable
            elif variable < MIN_LIMIT and variable > -MAX_LIMIT:
                return abs(variable)
            else:
                raise ValueError

        except Exception:
            print(f"Please, input a available option ({MIN_LIMIT} to finish the program, 0 for no limit and max of {MAX_LIMIT})")

def generateBits(firstBit: int, secondBit: int = None) -> int:
    floor = 2**firstBit
    ceil = 2**secondBit
    
    if secondBit == None:
        bit: int = secrets.randbits(firstBit)
    else:
        bit: int = secrets.randbelow(ceil - floor + 1) + floor
        
    return bit