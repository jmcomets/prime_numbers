"""prime_numbers.py - Tools for working with prime numbers"""
# -*- coding: utf-8 -*-

"""
Author: Jean-Marie Comets
Description: A series of optimized utility functions for prime
number computations, for example checking if a number is prime,
getting its prime number decomposition, etc...
"""

from functools import wraps, partial
import bitarray
import bisect
import math

def _check_factorizable_number_concept(n):
    """Checks basic assertions for a factorizable number,
    used for internal function checks, raising
    an AssertionError if it fails.
    """
    assert isinstance(n, int), 'Number must be an integer'
    assert n > 1, 'Number must be strictly greater than 1'

def _prime_sieve(n):
    """Returns a generator object corresponding to the
    sieve of Eratosthenes up to n (included).
    Help from here: http://stackoverflow.com/a/3035188/1441984
    """
    _check_factorizable_number_concept(n)
    yield 2
    # fix for including n in the sieve
    n += 1
    # shortcut to stay in the 80 columns
    ba = bitarray.bitarray
    sieve = ba(True for _ in xrange(n/2))
    # compute the sieves, excluding pair numbers
    for i in xrange(3, int(n**0.5) + 1, 2):
        if sieve[i/2]:
            # set multiples of this prime number as non prime
            s = ba(False for _ in xrange((n - i*i - 1)/(2*i) + 1))
            sieve[i*i/2::i] = s
    # return all the sieves
    for i in xrange(1, n/2):
        if sieve[i]:
            yield 2*i + 1

def checks_factorizable_number(f, type_msg='', value_msg=''):
    """Decorator provided to check the type/value of the sole input
    number argument, raising a TypeError if the given number isn't
    integral or a ValueError if it isn't a number striclty greater
    than 1. For the type-check, an explicit conversion to 'int' is
    done with the check that this newly converted number is the same
    as the input number (calling int(number) == number).
    The messages respectively for the TypeError/ValueError exceptions
    are the optional arguments type_msg/value_msg.
    """
    @wraps(f)
    def closure(number):
        try:
            n = int(number)
        except ValueError:
            raise TypeError(type_msg)
        if n != number:
            raise TypeError(type_msg)
        elif n <= 1:
            raise ValueError(value_msg)
        return f(n)
    return closure

# Internal prime number list used for faster computations
_initial_prime_list_max = 31622
_prime_list = tuple(_prime_sieve(_initial_prime_list_max))

def _opt_prime_sieve(n):
    """Optimized version of the similar function, also
    computing the prime sieve up to n (included).
    """
    _check_factorizable_number_concept(n)
    if n <= _prime_list[-1]:
        i = bisect.bisect_left(_prime_list, n)
        return _prime_list[:i]
    return _prime_sieve(n)

# Default message strings for concept checks
_type_msg = 'Number argument must be an integer'
_value_msg = 'Number argument must be strictly greater than 1'

# Internal decorator for concept checks
_checks_factorizable_number = partial(checks_factorizable_number,
        type_msg=_type_msg, value_msg=_value_msg)

@_checks_factorizable_number
def is_prime(number):
    """Check (and returns) if the given number is prime.
    This computation modifies the internal list of prime numbers, speeding
    up any computations for the entire module for prime numbers in this
    internal list.
    """
    # if prime is already in the list, just pick it
    if number <= _prime_list[-1]:
        i = bisect.bisect_left(_prime_list, number)
        return i != len(_prime_list) and _prime_list[i] == number
    # divide by each known prime
    limit = int(number ** .5)
    for p in _prime_list:
        if p > limit: return True
        if number % p == 0: return False
    # fall back on trial division if number too big
    for f in xrange(_initial_prime_list_max, limit, 6):
        if number % f == 0 or number % (f + 4) == 0:
            return False
    return True

def _trial_division_decompose(n):
    """Return a list of the prime factors for a natural number.
    Credit here: http://en.wikipedia.org/wiki/Trial_division
    """
    _check_factorizable_number_concept(n)
    # compute the prime sieve up to n
    primes = _opt_prime_sieve(n)
    # prime factors are stored in a dictionary { factor -> exponent }
    factors = {}
    # adding function is provided for reuse of following code
    def add_factor(f):
        if f not in factors:
            factors[f] = 0
        factors[f] += 1
    # actual algorithm try to divide n by each prime
    for p in primes:
        if p*p > n:
            break
        while n % p == 0:
            add_factor(p)
            n //= p
    # special case, n is a prime
    if n > 1:
        add_factor(n)
    return factors

@_checks_factorizable_number
def decompose(number):
    """Computes the prime number decomposition of a integral number,
    checking its type. A prime number decomposition is the dictionary
    { prime factor : exponent } excluding 1 and the input number itself.
    This computation modifies the internal list of prime numbers, speeding
    up any computations for the entire module for prime numbers in this
    internal list.
    """
    return _trial_division_decompose(number)
