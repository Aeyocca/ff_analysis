#!/bin/python
#11-12-19
#Alan E. Yocca
#fuck_kickers.py

from adjustRecords import adjustRecords as ar
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ctlFile")
args = parser.parse_args()

if __name__ == "__main__":

	#initialize
	#trade_comp = ta.tradeAnalyzer(args.ctlFile)
	#print("ctl file: %s" % (args.ctlFile))
	
	standing_adjuster = ar.adjustRecords(args.ctlFile)
	
	print("Current records:")
	standing_adjuster.currentStandings()

	print("Adjusted records:")
	standing_adjuster.adjustedStandings()