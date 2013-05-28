#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import prime_numbers

def display_prime_decomposition(number):
    """Displays the prime number decomposition
    of the given number.
    """
    dec = prime_numbers.decompose(number)
    print number, '->', dec

def exit(msg, errcode=1):
    """Prints the message to the standard output
    and exits with error code.
    """
    print msg
    sys.exit(errcode)

if __name__ == '__main__': # main program
    try:
        while True:
            number_str = raw_input().strip()
            if len(number_str) == 0:
                continue
            try:
                number = int(number_str)
            except ValueError:
                raise TypeError
            display_prime_decomposition(number)
    except TypeError:
        exit('Input must be an integer')
    except ValueError:
        exit('Input must be strictly greater than 1')
    except KeyboardInterrupt:
        exit('Interrupt')
    except EOFError: pass
