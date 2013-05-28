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
        large_prime = 87178291199
        msg = 'is_prime failed for large prime number %s' % large_prime
        ip = prime_numbers.is_prime
        self.assertTrue(ip(large_prime), msg)

class TestDecompose(unittest.TestCase):
    """TestCase for the decompose() function in the prime_numbers module.
    """
    def test_concepts(self):
        """Checks the edge cases due to bad input.
        """
        dec = prime_numbers.decompose
        self.assertRaises(TypeError, dec, 0.09)
        self.assertRaises(TypeError, dec, 6.90)
        self.assertRaises(TypeError, dec, '4.2')
        self.assertRaises(ValueError, dec, -42)
        self.assertRaises(ValueError, dec, 0)
        self.assertRaises(ValueError, dec, 1)

    def test_state_invariance(self):
        """Checks that the output doesn't depend on the state.
        """
        n = 1236
        msg = 'decompose failed state invariance test for input %s' % n
        dec = prime_numbers.decompose
        self.assertEqual(dec(n), dec(n), msg)

    def test_basic_numbers(self):
        """Checks some basic number decompositions.
        """
        dec = prime_numbers.decompose
        cases = {42: {2: 1, 3: 1, 7: 1}, 99: {3: 2, 11: 1,},
                1337: {7: 1, 191: 1}, 12456 : {2: 3, 3: 2, 173: 1}}
        for number, decomposition in cases.iteritems():
            found_dec = dec(number)
            msg = 'decompose failed for number %s : %s != %s' \
                    % (number, decomposition, dec)
            self.assertEqual(decomposition, found_dec, msg)

if __name__ == '__main__':
    unittest.main()
