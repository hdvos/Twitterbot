'''
Support functions for the twitterbot
TODO: write all the bookkeeping things in one file and design functions to read and write.
'''

import sys
import time


'''
pauses sthe program for set amount of minutes and prints out the nr of minutes left
Default pause is 15 mins
'''
def take_a_break(minutes = 15):
    print("take a break...\nzzzzzz.....\n")
    for i in range(minutes, 0, -1):
        sys.stdout.write("\r{} minutes until next tweet.".format(i))
        sys.stdout.flush()
        time.sleep(60)

    sys.stdout.write("\r0 minutes until next tweet.")
    sys.stdout.flush()
    print('\nGO!\n')


'''
writes the current date in a file.
This is used to check if program has already run today in case of a reboot.
'''
def write_checkfile(filename = ".checkfile.txt"):
    date = time.strftime("%d/%m/%Y")
    with open (filename, 'wt') as f:
        f.write(date)
        f.close()


'''
Compares if current date is equal to date in checkfile.
If a program is run for a second time on a day it returns false
Else True
'''
def is_reboot(filename = ".checkfile.txt"):
    date = time.strftime("%d/%m/%Y")
    with open (filename, 'rt') as f:
        check = f.read().strip()
        f.close()
    print (date, check)
    if date == check:
        return True
    else:
        return False

'''
Writes a file to keep track of how many tweets have been tweeted on a day.
'''
def write_counter_bookkeep(i, filename = ".counter_bookeep"):
    with open (filename, 'wt') as f:
        f.write(str(i))
        f.close()

'''
Reads the counter bookkeeping and returns the number of tweets that are posted on a day
'''
def get_counter(filename = ".counter_bookeep"):
    with open (filename, 'rt') as f:
        counter_str = f.read().strip()
        f.close()
    return int(counter_str)
