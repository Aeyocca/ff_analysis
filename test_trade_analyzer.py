#!/bin/python
#10-31-19
#Alan E. Yocca
#test_trade_analyzer.py

from tradeAnalyzer import tradeAnalyzer as ta
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ctlFile")
args = parser.parse_args()

if __name__ == "__main__":

	#print("arg: %s" % (args.ctlFile))
	
	#just want this
	trade_comp = ta.tradeAnalyzer(args.ctlFile)
	
	trade_comp.printOutput()
	



	
#	glob_vars = ta.tradeAnalyzer.readCTLfile(args.ctlFile)
#	out_table = []
#	table_1 = ta.tradeAnalyzer.multiplePlayers(glob_vars["player_list_one"],
#						glob_vars["week_start"],
#						glob_vars["week_end"],
#						glob_vars["leagueID"],
#						glob_vars["year"])
#	table_2 = ta.tradeAnalyzer.multiplePlayers(glob_vars["player_list_two"],
#						glob_vars["week_start"],
#						glob_vars["week_end"],
#						glob_vars["leagueID"],
#						glob_vars["year"])
#	
#	#something that creates the sum output table for player 1 and player 2
#	#shoot didn't differentiate between teams... diff out tables
#	
#	#could have attributes .table_1 and .table_2
#	#have these fed internally to compPlayers? I mean would we ever want to stop with
#	#table_1 and table_2, just feed this internally to trade analyzer
#	#have attribute be .trade_comp
#	
#	
#	trade_comp = []
#	trade_comp = ta.tradeAnalyzer.compPlayers(table_1, table_2)
#
#	print(trade_comp)

	#out_table.readCTLfile(args.ctlFile)
	#out_table.readCTLfile(args.ctlFile)
	
	#print(out_table)

#glob_vars = readCTLfile(ctl_file)
#		tradeAnalyzer.ctl_file = ctl_file
#		tradeAnalyzer.out_table = multiplePlayers(glob_vars["player_list_one"],
#							glob_vars["week_start"],
#							glob_vars["week_end"],
#							glob_vars["leagueID"],
#							glob_vars["year"])
#		tradeAnalyzer.out_table.append(multiplePlayers(glob_vars["player_list_two"],
#							glob_vars["week_start"],
#							glob_vars["week_end"],
#							glob_vars["leagueID"],
#							glob_vars["year"]))