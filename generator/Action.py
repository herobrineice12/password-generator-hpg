import pyperclip, secrets, sys, subprocess, platform

def showPassword(data_package) -> None:
    print(f"\n{data_package[0]}\n")
    try:
        copyPassword(data_package[0])
    except Exception as e:
        print(e)

def copyPassword(variable: str) -> None:
    if "termux" in platform.platform().lower():
        subprocess.run(['termux-clipboard-set'],variable)
    elif pyperclip.is_available:
        pyperclip.copy(variable)
    else:
        raise pyperclip.PyperclipException

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

def intInput(message: str, MIN_LIMIT: int = -1, MAX_LIMIT: int = 255) -> int:
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