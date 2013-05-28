"""test_prime_numbers.py - Unit tests for prime_numbers module"""
# -*- coding: utf-8 -*-

"""
Author: Jean-Marie Comets
Description: A series of unit tests using the unittest module,
checking basic and more complex test cases.
"""

import unittest
import prime_numbers

class TestIsPrime(unittest.TestCase):
    """TestCase for the is_prime() function in the prime_numbers module.
    """
    def test_concepts(self):
        """Checks the edge cases due to bad input.
        """
        ip = prime_numbers.is_prime
        self.assertRaises(TypeError, ip, 0.09)
        self.assertRaises(TypeError, ip, 6.90)
        self.assertRaises(TypeError, ip, '4.2')
        self.assertRaises(ValueError, ip, -42)
        self.assertRaises(ValueError, ip, 0)
        self.assertRaises(ValueError, ip, 1)

    def test_state_invariance(self):
        """Checks that the output doesn't depend on the state.
        """
        n = 42
        msg = 'is_prime failed state invariance test for input %s' % n
        ip = prime_numbers.is_prime
        self.assertEqual(ip(n), ip(n), msg)

    def test_basics_primes(self):
        """Checks basic prime cases.
        """
        basic_primes = [2, 3, 5, 7, 11, 13]
        ip = prime_numbers.is_prime
        for p in basic_primes:
            msg = 'is_prime failed for basic prime number %s' % p
            self.assertTrue(ip(p), msg)

    def test_basics_nonprimes(self):
        """Checks basic non-prime cases.
        """
        basic_nonprimes = [4, 6, 8, 9, 10, 12]
        ip = prime_numbers.is_prime
        for n in basic_nonprimes:
            msg = 'is_prime failed for basic non prime number %s' % n
            self.assertFalse(ip(n), msg)

    def test_large_prime(self):
        """Checks that is_prime works on a very large prime number.
        """
        pass # TODO

if __name__ == '__main__':
    unittest.main()
