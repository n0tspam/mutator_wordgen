#!/usr/bin/python3
#
# Simple script to mutate a word based on given parameters
# Supports l33tspeak, upper/lowercase mutation.
# Appends special characters, and incremental digits with or without padding
#
# Author - n0tspam

import re
import datetime
import argparse
from string import punctuation

parser = argparse.ArgumentParser(description='Wordlist mutation generator for specific words based on common password schemes.')

#required - keyword to mutate
requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument('-k','--keyword',action='store',dest='keyword', type=str, help='Keyword to mutate', required=True)

#optional params
parser.add_argument('-o','--outfile',action='store',dest='outfile', type=str, help='Output file')
parser.add_argument('-x','--special',action='store_true',default=False, help="Appends special characters at the end of string.")
parser.add_argument('-l','--l33t',action='store_true',default=False, help="o -> 0, e -> 3, i or l -> 1, s -> $, t -> 7")

#mutually exclusive parameters
group = parser.add_mutually_exclusive_group()
group.add_argument('-i', '--incmax', action='store', dest='intmax', type=int, help='Range of integers from 0 to <value>')
group.add_argument('-p', '--padmax', action='store', dest='padmax', type=int, help='Range of integers with padded value from 00 to <value>)')
group.add_argument('-s', '--start', action='store', dest='start_year', type=int, help="Takes 4 digits to represent a year,\
    and increments up until 5 years above present year. NOTE. will be appended prior to special chars set by -x flag (if applicable).")

#mutually exclusive parameters
group2 = parser.add_mutually_exclusive_group()
group2.add_argument('-up', '--upper', action='store_true', default=False, help="Sets keyword given to uppercase")
group2.add_argument('-lo', '--lower', action='store_true', default=False, help="Sets keyword given to lowercase")

args = parser.parse_args()

#validates the special param was set.
if args.special:
    special_chars = set(punctuation)
else:
    special_chars = []

#write function. either writes to file or standard out.
#also able to write to file by omitting the -outfile param and redirecting output
def print_out(keyword):
    try:
        if args.outfile:
            with open(args.outfile, 'a+') as outfile:
                outfile.write(keyword + "\n")
        else:
            print("%s" % keyword)
    except Exception:
        print("Error has occurred while writing to file. May be best to redirect output to file ./mutator.py [args] > wordlist.txt")

#based on param, sets upper/lower case
def check_case(keyword):
    if args.upper:
        up_keyword = keyword.upper()
        return up_keyword
    elif args.lower:
        low_keyword = keyword.lower()
        return low_keyword
    else:
        return False

#increments year until 5 years after the current year
def startyear_set(keyword, year, current_year):
    for num in range(int(year),int(current_year) + 6):
        #checks if special_chars param was set
        if len(special_chars) > 0:
            for char in special_chars:
                current_keyword = keyword + str(num) + char
                print_out(current_keyword)
        else:
            current_keyword = keyword + str(num)
            print_out(current_keyword)

#iterates through incrementation no padding
def increment_set(keyword):
    for num in range(0,args.intmax+1):
        #checks if special_chars param was set
        if len(special_chars) > 0:
            for char in special_chars:
                current_keyword = keyword + str(num) + char
                print_out(current_keyword)
        else:
            current_keyword = keyword + str(num)
            print_out("iteration - %s" % current_keyword)

#iterates through padding incrementation
def padded_set(keyword):
    string = len(str(args.padmax))
    #formats string for padding
    format = "{0:0=%sd}" % string
    for num in range(0,args.padmax+1):
        if len(special_chars) > 0:
            for char in special_chars:
                current_keyword = keyword + str(format.format(num)) + char
                print_out(current_keyword)
        else:
            current_keyword = keyword + str(format.format(num))
            print_out(current_keyword)

#changes keyword to l33tspeak based on substitutions below
def leet(keyword):
    leet_keyword = keyword.replace('e','3').replace('t','7').replace('o', '0').replace('i','1').replace('l', '1').\
    replace('s','$').replace('t','7')
    return leet_keyword

#main function
def main():
    #initialize current year for the -start parameter
    now = datetime.datetime.now()
    current_year = now.year

    #verifies via regex that the year is 4 digits
    if args.start_year:
        match = re.match("(^\d{4}$)", str(args.start_year))
        try:
            extracted_year = match.groups()[0]
            #verifies that the start year is equal to or below current year
            if (int(current_year) - int(extracted_year)) > -1:
                print("[+] Start year for incrementing - %s" % extracted_year)
            else:
                raise Exception("\n[-] Must be 4 digit year that's equal to or below the current year.\n")

        except Exception:
            print("\n[-] Make sure you're only entering a 4 digit year that's equal to or below the current year.\n")
            print(parser.print_help())
            exit()

    #initializes keyword to mutate
    current_keyword = args.keyword
    print("[+] Keyword to Mutate is: %s" % current_keyword)

    #detects l33t parameter
    if args.l33t:
        current_keyword = leet(current_keyword)
        print("[+] l33t mutation detected - %s" % current_keyword)

    #detects whether or not the case mutation argument was set
    if check_case(current_keyword):
        current_keyword = check_case(current_keyword)
        print("[+] Case change detected - %s" % current_keyword)

    #detects and calls function to increment without padding
    if args.intmax:
        increment_set(current_keyword)

    #detects and calls function to increment with padding
    elif args.padmax:
        padded_set(current_keyword)

    #detects and calls function to increment by year up to 5 years after current year
    elif args.start_year:
        startyear_set(current_keyword, extracted_year, current_year)

    #prints altered keyword with no repeated mutation
    else:
        print_out(current_keyword)

if __name__ == "__main__":
    main()
