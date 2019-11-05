#!/bin/python
#11-05-19
#Alan E. Yocca
#trade_analyzer.py

from tradeAnalyzer import tradeAnalyzer as ta
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ctlFile")
args = parser.parse_args()

if __name__ == "__main__":

	#initialize object, create final output
	trade_comp = ta.tradeAnalyzer(args.ctlFile)
	#print final output
	trade_comp.printOutput()
