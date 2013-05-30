"""prime_numbers.py - Tools for working with prime numbers"""
# -*- coding: utf-8 -*-

"""
Author: Jean-Marie Comets
Description: A series of optimized utility functions for prime
number computations, for example checking if a number is prime,
getting its prime number decomposition, etc...
"""

import functools as _ft
import numpy as _np
from bisect import bisect_left as _bl

def _check_factorizable_number_concept(n):
    """Checks basic assertions for a factorizable number,
    used for internal function checks, raising
    an AssertionError if it fails.
    """
    assert isinstance(n, int), 'Number must be an integer'
    assert n > 1, 'Number must be strictly greater than 1'

def _prime_sieve(n, use_np=False):
    """Returns a generator object corresponding to the
    sieve of Eratosthenes up to n (included).
    """
    _check_factorizable_number_concept(n)
    yield 2
    # fix including n in the sieve
    n += 1
    # on startup, no numbers are marked til n
    sieve = _np.zeros(n/2) if use_np else [0] * (n/2)
    # compute the sieves, excluding pair numbers
    for i in xrange(3, int(n**0.5) + 1, 2):
        if sieve[i/2] == 0:
            # yeild this prime number
            yield i
            # set multiples of this prime number as non prime
            for j in xrange(int(1.5*i), n/2, i):
                sieve[j] = 1

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
    @_ft.wraps(f)
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

def _make_global_sieve(n):
    """Internal function called on module import, returning
    a prime sieve list up to n (included).
    """
    return list(_prime_sieve(n))

# Internal prime number list used for faster computations
_global_sieve_initial_max = 1000000
_global_sieve = _make_global_sieve(_global_sieve_initial_max)
_global_sieve_max_size = 1000000
# Startup check so _global_sieve_initial_max and _global_sieve_max_size
# work well together (since they are fixed at runtime)
assert len(_global_sieve) < _global_sieve_max_size

def _max_global_sieve():
    """Internal function returning the highest element in the
    global sieve.
    """
    return _global_sieve[-1]

def _in_global_sieve(n):
    """Internal function returning if the number is in the global
    prime sieve list, without checking any concepts on the number.
    """
    if n <= _max_global_sieve():
        i = _bl(_global_sieve, n)
        if i != len(_global_sieve) and _global_sieve[i] == n:
            return True
    return False

def _add_to_global_sieve(n):
    """Internal function appending a prime number to the global
    sieve, checking that this list is under its maximum size.
    Simply returns True if the number was actually added, False
    otherwise. No checking is done on the number's prime property,
    only the 'factorizable number' concept is checked, along with
    the fact that the item isn't already in the list.
    """
    _check_factorizable_number_concept(n)
    assert_msg = 'Cannot add %s to the global sieve : already exists' % n
    assert not _in_global_sieve(n), assert_msg
    if len(_global_sieve) < _global_sieve_max_size:
        _global_sieve.append(n)
        return True
    return False

def _opt_prime_sieve(n):
    """Optimized version of the similar function, also
    computing the prime sieve up to n (included).
    Returns a generator object.
    """
    _check_factorizable_number_concept(n)
    # helper that returns a generator, appending to the
    # global prime sieve list if this one doesn't the number
    def yield_and_append(sieve):
        for s in sieve:
            if not _in_global_sieve(s):
                _add_to_global_sieve(s)
            yield s
    # helper that returns a generator of prime numbers up to
    # the given number (included)
    def yield_til_number(number):
        for p in _global_sieve:
            yield p
            if p >= number:
                break
    # if the number is already in our list yield its sieve
    if _in_global_sieve(n):
        return yield_til_number(n + 1)
    else:
        return yield_and_append(_prime_sieve(n))

# Default message strings for concept checks
_type_msg = 'Number argument must be an integer'
_value_msg = 'Number argument must be strictly greater than 1'

# Internal decorator for concept checks
_checks_factorizable_number = _ft.partial(checks_factorizable_number,
        type_msg=_type_msg, value_msg=_value_msg)

@_checks_factorizable_number
def is_prime(number):
    """Check (and returns) if the given number is prime.
    This computation modifies the internal list of prime numbers, speeding
    up any computations for the entire module for prime numbers in this
    internal list.
    """
    # already in the global sieve -> prime
    if _in_global_sieve(number):
        return True
    # divide by each known prime until square root
    limit = int(number ** .5)
    for p in _global_sieve:
        # iteration is over square root -> prime
        if p > limit:
            return True
        # divisible by prime -> not prime
        if number % p == 0:
            return False
    # fall back on trial division if number too big
    # fix for iteration skipping 2/3 multiples
    start = _max_global_sieve()
    if (start + 2) % 3 == 0:
        if number % start == 0:
            return False
        start += 4
    # trial division with iteration skipping 2/3 multiples
    for f in xrange(start, limit, 6):
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
