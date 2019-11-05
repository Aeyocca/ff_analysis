#!/bin/python
#10-31-19
#Alan E. Yocca
#tradeAnalyzer.py
#how to make this a callable class

import json
import sys
import re
import pandas
    
#loop through to find the name, shit gotta read all player names
#"fullName"

#lets write a class that goes through, extracts meta data for a player, just massaging data
#player class that extracts the attributes we really want
#eh just kind of condenses this json
#want really clean code to plug into different things
#yea get a class that reads in a file and returns a players points, yards, receiving, and tds

class tradeAnalyzer:
	def __init__(self,ctl_file):
		#glob_vars = readCTLfile(ctl_file)
		#tradeAnalyzer.out_table = []
		#tradeAnalyzer.out_table = multiplePlayers(glob_vars["player_list_one"],
		#					glob_vars["week_start"],
		#					glob_vars["week_end"],
		#					glob_vars["leagueID"],
		#					glob_vars["year"])
		#tradeAnalyzer.out_table.append(multiplePlayers(glob_vars["player_list_two"],
		#					glob_vars["week_start"],
		#					glob_vars["week_end"],
		#					glob_vars["leagueID"],
		#					glob_vars["year"]))
		tradeAnalyzer.ctl_file = ctl_file
		
	def readCTLfile(ctl_file):
		#return dictionary? with control file variables
		glob_vars = []
		with open(ctl_file) as file:
			glob_vars = json.load(file)
		
		#print("var: %s" % (glob_vars["leagueID"]))
		return glob_vars
		
	def multiplePlayers(player_array, week_start, week_end, leagueID, year):
		#loop through player array, put them all in one table
		out_dict = []
		
		#print("player_array len: %s" % (len(player_array)))
		for player in player_array:
		
			#print("Calling playerStats")
			out_dict = out_dict + tradeAnalyzer.playerStats(player,week_start,
							week_end,leagueID,year)
			#print("done calling player stats")
			#print("Player stats: %s" % (out_dict))
		
		return out_dict

	def playerStats(player, week_start, week_end, leagueID, year):
		#table tidy, can add more than one player
		#Player_name	Week	Score	Yds	Rec	Tds

		#print("hello")

		all_weeks = tradeAnalyzer.loadData(week_start, week_end, leagueID, year)
		
		#print("all weeks: %s" % (all_weeks))
			
		player_dict = tradeAnalyzer.findPlayer(all_weeks, player)

		#print("player dict: %s" % (player_dict))
		#print("player: %s" % (player))
		
		stat_array = tradeAnalyzer.extractStats(player_dict)   		
   		
		#print("stat array: %s" % (stat_array))
		
		return stat_array
   		
   		
	def loadData(week_start, week_end, leagueID, year):
		#load data into dictionary between given weeks
		out_dict = []
		for i in range(week_start,week_end,1):
			#print("week: %s" % (i))
		
			box_file = ("boxscores/boxscores_" + str(leagueID) + "_" + str(year)
						+ "_" + str(i) + "_" + str(i) + ".json")
			weekly_data = []
			with open(box_file) as file:
				weekly_data = json.load(file)
			
			#print("loadData: %s" % (weekly_data[1]["homeRoster"][1]["player"]["fullName"]))

			out_dict = out_dict + weekly_data
		
		#print("loadData: %s" % (out_dict[1]["homeRoster"][1]["player"]["fullName"]))
		
		if len(out_dict) == 0:
			print("Length of dictionary is zero (%s)" % (len(out_dict)))
			print("Perhaps trying to load in weeks that have yet to occur?")
		
		return out_dict
	
	def findPlayer(data, player):
		#perhaps this merges with extractStats eventually..
		#this could be useful if want different information?
		#looks prettier as separate function
		#takes in full week boxscore json
		#returns dictionary with desired player's information
		out_dict = []
		
		#print("keys: %s" % (data[1][1]))
		#print("Looking for player: %s" % (player))
		
		for i in range(len(data)):
			for j in range(len(data[i]["homeRoster"])):
			
				#tmp = data[i]["homeRoster"][j]["player"]["fullName"]
				#tmp = data[i]["homeRoster"][j]["player"]["fullName"]
				#tmp_len = len(tmp)
				
				#if tmp_len > 1:
				#print("Length > 1: %s" % (tmp_len))
				#print("values: %s" % (tmp))
				#sys.exit()

				if data[i]["homeRoster"][j]["player"]["fullName"] == player:					
					#print("Found him! %s" % 
					#	(data[i]["homeRoster"][j]["player"]["fullName"]))

						
					#print("player: %s" % (player))
		
					out_dict.append(data[i]["homeRoster"][j])
					
			for k in range(len(data[i]["awayRoster"])):
				if data[i]["awayRoster"][k]["player"]["fullName"] == player:
					#print("Found him! %s" % 
					#	(data[i]["awayRoster"][k]["player"]["fullName"]))
		
					out_dict.append(data[i]["awayRoster"][k])
					
		if len(out_dict) == 0:
			print("Could not locate player: %s" % (player))
			print("Did you spell it correctly?")
			#exit
		
		return out_dict

	def extractStats(df):
		#feed in dictionary with data we need
		#also feed in fields we wont find in json because we are returning array
		#to add as line to tidy table
		#actually could add to array later
		#this could be named dictionary we can stick together
		stat_dict = []
		
		#print("df len: %s" % (len(df)))
		for i in range(len(df)):

			#print("keys: %s" % (df[i]["rawStats"]))			
			
			#I should make these keys instead of array
			
			fN = df[i]["player"].get("fullName") # 0
			dP = df[i]["player"].get("defaultPosition") # 1
			wP = df[i].get("position") # 2
			tP = df[i].get("totalPoints") # 3
			ruY = df[i]["rawStats"].get("rushingYards", 0) # 4
			ruT = df[i]["rawStats"].get("rushingTouchdowns", 0) # 5
			reY = df[i]["rawStats"].get("receivingYards", 0) # 6
			re = df[i]["rawStats"].get("receivingReceptions", 0) # 7
			reT = df[i]["rawStats"].get("receivingTouchdowns", 0) # 8

			stat_dict.append({"fullName" : fN, "defaultPosition" : dP,
			"startedPosition" : wP, "totalPoints" : tP, "rushingYards" : ruY,
			"rushingTouchdowns" : ruT, "receivingYards" : reY,
			"receivingReceptions" : re, "receivingTouchdowns" : reT})
			
		return stat_dict



		
	def compPlayers(table_1, table_2):
		table_1_weeks = tradeAnalyzer.collapseAcrossWeeks(table_1)
		table_2_weeks = tradeAnalyzer.collapseAcrossWeeks(table_2)
		
		print("table_1_weeks: %s" % (table_1_weeks))
		
		table_1_players = tradeAnalyzer.collapseAcrossPlayers(table_1_weeks)
		table_2_players = tradeAnalyzer.collapseAcrossPlayers(table_2_weeks)
		
		print("table_1_players: %s" % (table_1_players))
		
		#these should be final output tables..
		comb_table = tradeAnalyzer.combineTables(table_1_players,table_2_players)

		return comb_table		
				
	def collapseAcrossWeeks(df):
		#stat arrays should have one row per player
		#fullName defPos, Pos, total Pts, ruY, ruT, reY, re, reT
		#make dictionary to collapse all weeks to single values
		
		#sum within players
		out_dict = {}
		
		for i in range(len(df)):
			started = 0
			#fullName equal to all other values
			#for started points easy here can just not add pts

			#if we already ran into this player
			if df[i]["fullName"] in out_dict.keys():
				#add to
				
				out_dict[df[i]["fullName"]]["Total TDs"] += (df[i]["rushingTouchdowns"] + 
														df[i]["receivingTouchdowns"])
				out_dict[df[i]["fullName"]]["Total ruY"] += int(df[i]["rushingYards"])
				out_dict[df[i]["fullName"]]["Total reY"] += int(df[i]["receivingYards"])
				out_dict[df[i]["fullName"]]["Total rec"] += int(df[i]["receivingReceptions"])
				out_dict[df[i]["fullName"]]["Total pts"] += int(df[i]["totalPoints"])
				
				if df[i]["startedPosition"] != "Bench":
					#add to started and started per game
					started += 1
					out_dict[df[i]["fullName"]] = (tradeAnalyzer.initializeKey(
						out_dict[df[i]["fullName"]],"Pts Started", 0))
					out_dict[df[i]["fullName"]] = (tradeAnalyzer.initializeKey(
						out_dict[df[i]["fullName"]],"Total Starts", 0))
						
					out_dict[df[i]["fullName"]]["Pts Started"] += df[i]["totalPoints"]
					out_dict[df[i]["fullName"]]["Total Starts"] += started

			else:
				#initialize

				print("rec td: %s" % (df[i]["receivingTouchdowns"]))
				print("rus td: %s" % (df[i]["rushingTouchdowns"]))
				
				print("player array num: %s" % (i))
				print("player: %s" % (df[i]["fullName"]))
				print("type: %s" % (type(df[i]["rushingTouchdowns"])))

				#tmp = sum(0 + 0)
				
				out_dict[df[i]["fullName"]] = {"Total TDs" : (df[i]["rushingTouchdowns"] + 
												df[i]["receivingTouchdowns"]),
												"Total ruY" : int(df[i]["rushingYards"]),
												"Total reY" : int(df[i]["receivingYards"]), 
												"Total rec" : int(df[i]["receivingReceptions"]),
												"Total pts" : int(df[i]["totalPoints"])}
				
				if df[i]["startedPosition"] != "Bench":
					#add to started and started per game
					started += 1
					out_dict[df[i]["fullName"]] = (tradeAnalyzer.initializeKey(
						out_dict[df[i]["fullName"]],"Pts Started", 0))
					out_dict[df[i]["fullName"]] = (tradeAnalyzer.initializeKey(
						out_dict[df[i]["fullName"]],"Total Starts", 0))
						
					out_dict[df[i]["fullName"]]["Pts Started"] += df[i]["totalPoints"]
					out_dict[df[i]["fullName"]]["Total Starts"] += started
					

		games=(len(df) / len(out_dict.keys()))
		for key in out_dict.keys():
			out_dict[key]["Total Games"] = games

		print("out_dict: %s" % (out_dict))
		
		return out_dict
		
	def initializeKey(df, key, init):
		if key not in df.keys():
			df[key] = init
		return df
		
	def collapseAcrossPlayers(df):
		#now sum across players, skip bench players for started stats
		team_sums = {}
		for player in df:
			team_sums = (tradeAnalyzer.initializeKey(
						team_sums,"Players", ""))
			
			team_sums["Players"] += str(player + " \n")
			
			print("df[player]: %s" % (df[player]))
			
			
			for stat in df[player]:
				team_sums = (tradeAnalyzer.initializeKey(
						team_sums,stat, 0))
				team_sums[stat] += df[player][stat]



		team_sums["Pts per player"] = team_sums["Total pts"] / len(df)
		team_sums["Pts per player Started"] = team_sums["Pts Started"] / team_sums["Total Starts"]
		
		return team_sums

	def combineTables(df1,df2):
	
		print("df1: %s" % (df1))
	
		col_names = ["Team 1", "Team 2", "Difference"]
		row_names = df1.keys()
		difference = []
		for key in df1.keys():
			if isinstance(df1[key], int):
				difference.append(df1[key] - df2[key])
			else:
				difference.append("N/A")
		
		data = [df1.values(), df2.values(), difference]
		output = pandas.DataFrame(data,col_names,row_names)
		return output
		

#		Team 1		Team 2	Difference
#Players	keys
#Total TDs	5+8
#Total RuYds	4
#Total Rec	7
#Total Rec Yds	6
#Total Pts	3
#Pts per player
#Pts Started
#Pts/plyr started













