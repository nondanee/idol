# -*- coding: utf-8 -*-

import sys, argparse
import capture, database
    
parser = argparse.ArgumentParser()
parser.add_argument(
    '-p', metavar = 'page', dest = 'page',
    default = 1, type = int,
    help = 'specify page number'
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-k', dest = 'keyakizaka', action = 'store_true',
    help = 'capture keyakizaka only'
)
group.add_argument(
    '-n', dest = 'nogizaka', action = 'store_true',
    help = 'capture nogizaka only'
)
args = parser.parse_args()

connect = database.connect()

if args.nogizaka:
    capture.deal(connect, capture.nogizaka_only(args.page))
elif args.keyakizaka:
    capture.deal(connect, capture.keyakizaka_only(args.page))
else:
    capture.deal(connect, capture.both())

connect.close()
