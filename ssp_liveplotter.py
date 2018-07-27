#!/usr/bin/python3

import datetime
import matplotlib
import subprocess
import sys
import time

def main():
    print('Live plotting tool for ssp')

    now = datetime.datetime.utcnow()

    filename = './logs/{}_{}_{}.log'.format(now.year, now.month, now.day)
    proc_tail = subprocess.Popen(['tail', '-F', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        line = proc_tail.stdout.readline()
        print(str(line, 'utf-8'), end='')

if __name__ == '__main__':
    main()
    sys.exit()
