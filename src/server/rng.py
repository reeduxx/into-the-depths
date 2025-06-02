import random
from typing import Sequence, Any

class RNG:
    """
    A deterministic random number generator.

    Wraps Python's 'random.Random' and ensures reproducible 
    random values when initialized with a fixed seed.

    Attributes:
        _rng (random.Random): The seeded RNG instance.
    """
    def __init__(self, seed: int):
        """
        Initializes the deterministic RNG with a seeded instance.

        Args:
            seed (int): The initial seed for the RNG.
        """
        self._rng = random.Random(seed)
    
    def randint(self, a: int, b: int) -> int:
        """
        Returns a random integer N such that a <= N <= b.

        Args:
            a (int): The lower bound (inclusive).
            b (int): The upper bound (inclusive).
        
        Returns:
            int: A random integer between a and b.
        """
        return self._rng.randint(a, b)

    def choice(self, seq: Sequence) -> Any:
        """
        Returns a random element from the sequence.
        
        Args:
            seq (Sequence): A non-empty sequence (list, tuple, etc.).

        Returns:
            Any: A random element from the sequence.
        """
        return self._rng.choice(seq)