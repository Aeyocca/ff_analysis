#!/bin/python
#10-31-19
#Alan E. Yocca
#test_point_calculator.py
#how to make this a callable class

import json
    
#loop through to find the name, shit gotta read all player names
#"fullName"

#lets write a class that goes through, extracts meta data for a player, just massaging data
#player class that extracts the attributes we really want
#eh just kind of condenses this json
#want really clean code to plug into different things
#yea get a class that reads in a file and returns a players points, yards, receiving, and tds

class tradeAnalyzer:
	def __init__(self)
		tradeAnalyzer.week_start = week_start
		tradeAnalyzer.week_end = week_end
		#hopefully get these variables from ctl file

	def readCTLfile (ctl_file):
		#return dictionary? with control file variables
		glob_vars = []
		with open(ctl_file) as file:
			glob_vars.append(read(file))
		return glob_vars
		
	def multiplePlayers (player_array, week_start, week_end):
		#loop through player array, put them all in one table
		out_dict = []
		for player in player_array:
			out_dict.append(playerStats(player,week_start,week_end))

	def playerStats (player,week_start,week_end):
		#table tidy, can add more than one player
		#Player_name	Week	Score	Yds	Rec	Tds

		all_weeks = loadData(week_start,week_end,leagueID,year)	
   		player_dict = findPlayer(all_weeks, player)
   		stat_array = extractStats(player_dict)   		
   		
	def loadData(week_start,week_end,leagueID,year):
		#load data into dictionary between given weeks
		out_dict = []
		for i in range(week_start,week_end,1):
			box_file = ("boxscores/boxscores_" + leagueID + "_" + year
						+ "_" + i + "_" + i + ".json")
			weekly_data = []
			with open(box_file) as file:
				weekly_data = json.load(file)
			out_dict.append(weekly_data)
		
		if len(out_dict) == 0:
			print("Length of dictionary is zero (%s)" % (len(out_dict)))
			print("Perhaps trying to load in weeks that have yet to occur?")
		
		return out_dict
	
	def findPlayer(df, player):
		#perhaps this merges with extractStats eventually..
		#this could be useful if want different information?
		#looks prettier as separate function
		#takes in full week boxscore json
		#returns dictionary with desired player's information
		out_dict = []
		for i in range(len(data)):
			for j in range(len(data[i]["homeRoster"])):
				if data[i]["homeRoster"][j]["player"]["fullName"] == player:					
					#print("Found him! %s" % 
					#	(data[i]["homeRoster"][j]["player"]["fullName"]))
					out_dict.append(data[i]["homeRoster"][j])
					
			for k in range(len(data[i]["awayRoster"])):
				if data[i]["awayRoster"][k]["player"]["fullName"] == player:
					#print("Found him! %s" % 
					#	(data[i]["homeRoster"][j]["player"]["fullName"]))
					out_dict.append(data[i]["awayRoster"][j])
				
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
		for i in range(df):
			fN = df[i]["player"]["fullName"]
			dP = df[i]["player"]["defaultPosition"]
			tP = df[i]["position"]
			ruY = df[i]["rawStats"]["rushingYards"]
			ruT = df[i]["rawStats"]["rushingTouchdowns"]
			reY = df[i]["rawStats"]["receivingYards"]
			re = df[i]["rawStats"]["receivingReceptions"]
			reT = df[i]["rawStats"]["receivingTouchdowns"]
			stat_dict[i] = [fN, dP, tP, ruY, ruT, reY, re, reT]
		return stat_dict
		
				

#"player"
#	"fullName"
#	"defaultPosition"
#"position"
#"totalPoints"
#"rawStats"
#	"rushingYards"
#	"rushingTouchdowns"
#	"receivingYards"
#	"receivingReceptions"
					

#print("Done")


















