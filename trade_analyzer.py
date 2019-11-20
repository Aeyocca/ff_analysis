#!/bin/python
#11-05-19
#Alan E. Yocca
#trade_analyzer.py

from tradeAnalyzer import tradeAnalyzer as ta
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ctlFile")
parser.add_argument("--week_start", nargs="?", type = int)
parser.add_argument("--week_end", nargs="?", type = int)
parser.add_argument("--player_list_one", nargs="?", help = "comma separated list")
parser.add_argument("--player_list_two", nargs="?", help = "comma separated list")
args = parser.parse_args()

if __name__ == "__main__":

	#initialize object, create final output
	trade_comp = ta.tradeAnalyzer(args.ctlFile)
	#print final output

	trade_comp.adjustArgs(week_start = args.week_start,
							week_end = args.week_end,
							player_list_one = args.player_list_one.split(","),
							player_list_two = args.player_list_two.split(","))

	trade_comp.createOutput()
	trade_comp.printOutput()
