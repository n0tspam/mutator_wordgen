# mutator_wordgen
Mutator to generate a wordlist for bruteforce attack

usage: mutator.py [-h] -k KEYWORD [-o OUTFILE] [-x] [-l]
                  [-i INTMAX | -p PADMAX | -s START_YEAR] [-up | -lo]

Wordlist mutation generator for specific words based on common password
schemes.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Output file
  -x, --special         Appends special characters at the end of string.
  -l, --l33t            o -> 0, e -> 3, i or l -> 1, s -> $, t -> 7
  -i INTMAX, --incmax INTMAX
                        Range of integers from 0 to <value>
  -p PADMAX, --padmax PADMAX
                        (Range of integers with padded value from 00 to
                        <value>)
  -s START_YEAR, --start START_YEAR
                        Takes 4 digits to represent a year, and increments up
                        until 5 years above present year. NOTE. will be
                        appended prior to special chars set by -x flag (if
                        applicable).
  -up, --upper          Sets keyword given to uppercase
  -lo, --lower          Sets keyword given to lowercase

Required named arguments:
  -k KEYWORD, --keyword KEYWORD
                        Keyword to mutate
