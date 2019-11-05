#!/bin/python
#10-31-19
#Alan E. Yocca
#tradeAnalyzer.py
#how to make this a callable class

import json
import sys
import re
import pandas
import numpy
    
#loop through to find the name, shit gotta read all player names
#"fullName"

#lets write a class that goes through, extracts meta data for a player, just massaging data
#player class that extracts the attributes we really want
#eh just kind of condenses this json
#want really clean code to plug into different things
#yea get a class that reads in a file and returns a players points, yards, receiving, and tds

class tradeAnalyzer:
	def __init__(self,ctl_file):
		self.ctl_file = ctl_file
		self.glob_vars = self.readCTLfile(self.ctl_file)
		self.table_1 = self.multiplePlayers(self.glob_vars["player_list_one"],
						self.glob_vars["week_start"],
						self.glob_vars["week_end"],
						self.glob_vars["leagueID"],
						self.glob_vars["year"])
		
		self.table_2 = self.multiplePlayers(self.glob_vars["player_list_two"],
						self.glob_vars["week_start"],
						self.glob_vars["week_end"],
						self.glob_vars["leagueID"],
						self.glob_vars["year"])
		
		self.trade_comp = self.compPlayers(self.table_1,self.table_2)
	
	def printOutput(self):
		print("%s" % (self.trade_comp))
			
	def readCTLfile(self,ctl_file):
		#return dictionary? with control file variables
		glob_vars = []
		with open(ctl_file) as file:
			glob_vars = json.load(file)
		
		return glob_vars
		
	def multiplePlayers(self, player_array, week_start, week_end, leagueID, year):
		#loop through player array, put them all in one table
		out_dict = []
		
		for player in player_array:
		
			out_dict = out_dict + tradeAnalyzer.playerStats(player,week_start,
							week_end,leagueID,year)
		
		return out_dict

	def playerStats( player, week_start, week_end, leagueID, year):
		#table tidy, can add more than one player
		#Player_name	Week	Score	Yds	Rec	Tds

		all_weeks = tradeAnalyzer.loadData(week_start, week_end, leagueID, year)
		
		player_dict = tradeAnalyzer.findPlayer(all_weeks, player)
		
		stat_array = tradeAnalyzer.extractStats(player_dict)   		
		
		return stat_array
   		
   		
	def loadData( week_start, week_end, leagueID, year):
		#load data into dictionary between given weeks
		out_dict = []
		for i in range(week_start,(week_end + 1),1):
			box_file = ("boxscores/boxscores_" + str(leagueID) + "_" + str(year)
						+ "_" + str(i) + "_" + str(i) + ".json")
			weekly_data = []
			with open(box_file) as file:
				weekly_data = json.load(file)

			out_dict = out_dict + weekly_data
		
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
		
		for i in range(len(data)):
			for j in range(len(data[i]["homeRoster"])):
				if data[i]["homeRoster"][j]["player"]["fullName"] == player:					
					out_dict.append(data[i]["homeRoster"][j])
					
			for k in range(len(data[i]["awayRoster"])):
				if data[i]["awayRoster"][k]["player"]["fullName"] == player:
					out_dict.append(data[i]["awayRoster"][k])
					
		if len(out_dict) == 0:
			print("Could not locate player: %s" % (player))
			print("Did you spell it correctly?")
		
		return out_dict

	def extractStats(df):
		#feed in dictionary with data we need
		#also feed in fields we wont find in json because we are returning array
		#to add as line to tidy table
		#actually could add to array later
		#this could be named dictionary we can stick together
		stat_dict = []
		
		for i in range(len(df)):
			
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

	def compPlayers(self, table_1, table_2):
		table_1_weeks = tradeAnalyzer.collapseAcrossWeeks(table_1)
		table_2_weeks = tradeAnalyzer.collapseAcrossWeeks(table_2)
		
		table_1_players = tradeAnalyzer.collapseAcrossPlayers(table_1_weeks)
		table_2_players = tradeAnalyzer.collapseAcrossPlayers(table_2_weeks)
		
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
				out_dict[df[i]["fullName"]]["Total ruY"] += df[i]["rushingYards"]
				out_dict[df[i]["fullName"]]["Total reY"] += df[i]["receivingYards"]
				out_dict[df[i]["fullName"]]["Total rec"] += df[i]["receivingReceptions"]
				out_dict[df[i]["fullName"]]["Total pts"] += df[i]["totalPoints"]
				
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

				out_dict[df[i]["fullName"]] = {"Total TDs" : (df[i]["rushingTouchdowns"] + 
												df[i]["receivingTouchdowns"]),
												"Total ruY" : df[i]["rushingYards"],
												"Total reY" : df[i]["receivingYards"], 
												"Total rec" : df[i]["receivingReceptions"],
												"Total pts" : df[i]["totalPoints"]}
				
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
			
			team_sums["Players"] += str(player + " ")
			
			for stat in df[player]:
				team_sums = (tradeAnalyzer.initializeKey(
						team_sums,stat, 0))
				
				#print("player: %s" % (player))
				#print("stat: %s" % (stat))
				#print("value: %s" % (df[player][stat]))
				team_sums[stat] += df[player][stat]

		team_sums["Pts per player"] = team_sums["Total pts"] / len(df)
		team_sums["Pts per player Started"] = team_sums["Pts Started"] / team_sums["Total Starts"]
		
		return team_sums

	def combineTables(df1,df2):
	
		col_names = ["Team 1", "Team 2", "Difference"]
		row_names = list(df1.keys())
		difference = []
		df1_value = []
		df2_value = []
		
		for key in df1.keys():
			df1_value.append(df1[key])
			df2_value.append(df2[key])
			try:
				difference.append(df1[key] - df2[key])
			except:
				difference.append("N/A")
		
		#data = [list(df1.values()), list(df2.values()), difference]
		#above line would have been nice, but the order gets messed up, so wrote it out above
		data = [df1_value, df2_value, difference]
		
		#wrap player names by adding dummy row with empty strings
		data = tradeAnalyzer.splitPlayers(data,row_names)
		
		output = pandas.DataFrame(data,col_names,row_names)
		out_trans = pandas.DataFrame.transpose(output)
		return out_trans
	
	def splitPlayers(data,row_names):			
		#get player array
		#loop through larger of the player arrays
		#insert empty row
		
		#print("data: %s" % (data))
		
		player1_split = data[0][0].split()
		player1_by_player = []
		
		#print("player split: %s" % (player1_split))
		#print("length: %s" % (len(player1_split)))
		
		for i in range(0,len(player1_split),2):
			
			player1_by_player.append((player1_split[i] + " " +
										player1_split[(i + 1)]))
		
		player2_split = data[1][0].split()
		player2_by_player = []
		for i in range(0,len(player2_split),2):
			player2_by_player.append((player2_split[i] + " " +
										player2_split[(i + 1)]))
		
		num_players = max(len(player2_by_player),len(player1_by_player))
										
		for i in range(num_players):
			#don't add row for first iteration
			if i == 0:
				data[0][0] = player1_by_player[i]
				data[1][0] = player2_by_player[i]
			
			else:
				try:
					data[0].insert(1,player1_by_player[i])
				except:
					data[0].insert(1,"")

				try:
					data[1].insert(1,player2_by_player[i])
				except:
					data[1].insert(1,"")
					
				data[2].insert(1,"")
				row_names.insert(1,"")

		return data
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		


