from .Action import generateBits
from multiprocessing import Pool

class PrimeGen:
    @staticmethod
    def primeCounter(rounds: int, start: int = generateBits(20,21)) -> str:
        limit: int = start + rounds
        salt: str = ""

        if start % 2 == 0: start += 1

        candidates = [i for i in range(start, limit, 2)
                      if i % 3 != 0 and i % 5 != 0 and i % 7 != 0]

        with Pool() as pool:
            results = pool.map(PrimeGen.primeCheck,candidates)        

        for num, is_prime in zip(candidates, results):
            if is_prime:
                salt += str(num)

        return salt
    
    @staticmethod
    def primeCheck(number: int) -> bool:
        for i in range(11, int(number ** 0.5) + 1, 2):
            if number % i == 0: return False
        
        return True