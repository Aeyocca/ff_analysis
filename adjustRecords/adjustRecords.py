#!/bin/python
#11-12-19
#Alan E. Yocca
#adjustedRecords.py
#try to make generalizable to other things...
#main idea is what standings would be without kickers

import sys
sys.path.append("../tradeAnalyzer")
import pandas
import numpy
#import tradeAnalyzer as ta
from tradeAnalyzer import tradeAnalyzer as ta
import warnings
import json


#function to extract matchup stats
#list:
#Matchup X
#	Team n
#		Player
#		Position
#		Points
#		TotalPoints
#	Team p

#then can write function to remove specified position and recalculate records

#also need function to translate team names.... probs hardcode that in a file
#do this last

#then do a "points from position" function

class adjustRecords:
	def __init__(self,ctl_file):
		self.ctl_file = ctl_file
		self.ta_funs = ta.tradeAnalyzer(self.ctl_file)
		self.glob_vars = self.ta_funs.readCTLfile(self.ctl_file)

	def currentStandings(self):
		league_data = self.loadData(self.glob_vars["week_start"],
									self.glob_vars["week_end"],
									self.glob_vars["leagueID"],
									self.glob_vars["year"])
		curr_records = self.calculateRecords(league_data)
		#how to get this to pretty table....
		curr_records = self.translateTeams(curr_records,self.glob_vars["Team Translations"])
		output = self.recordsToStandings(curr_records)
		print("%s" % (output))
	
	def adjustedStandings(self):
		league_data = self.loadData(self.glob_vars["week_start"],
									self.glob_vars["week_end"],
									self.glob_vars["leagueID"],
									self.glob_vars["year"])
		curr_records = self.calculateRecords(league_data)
		curr_records_trans = self.translateTeams(curr_records,self.glob_vars["Team Translations"])
		
		adj_scores = self.adjustScore(league_data, self.glob_vars["drop_position"])
		adj_records = self.calculateRecords(adj_scores)
		adj_records_trans = self.translateTeams(adj_records,self.glob_vars["Team Translations"])

		#how to get this to pretty table....
		output = self.recordsToStandings(adj_records_trans)
		
		adj_rec_trans_diff = self.addDiffCol(curr_records_trans,output)
		
		
		print("%s" % (adj_rec_trans_diff))
		
	def translateTeams(self,data,trans_dict):
		#translate records object keys
		new_records = {}
		for team_number in data.keys():
			try:
				new_records[trans_dict[str(team_number)]] = data[team_number]
			except:
				print("Cannot find translation for team number: %s" % (team_number))
				
		return new_records
		
	def addDiffCol(self,curr_records_trans,adj_data_output):
		#add column to adjusted records table
		#make vector with differences
		diff = []
			
		#print("adj: %s" % (adj_data_output))
		
#		for key in adj_data_output.keys():
		for i in range(1,(len(adj_data_output) + 1)):
			loop_diff = curr_records_trans[adj_data_output["Team"][i]]["totalPoints"] - adj_data_output["Points For"][i]
			diff.append(loop_diff)
		
		adj_data_output["Difference"] = diff
		
		return adj_data_output

	def recordsToStandings(self,data):
		#sort by wins, then by totalPoints
		#eh could edit code to make it a table in the first place...
		#now I think dictionary is best way to do it
		#convert to table first
		#team, wins, losses, total points
		record_table = []
		
		for team in data.keys():
			record_table.append([team,
								data[team]["wins"],
								data[team]["losses"],
								data[team]["totalPoints"]])
		#sort record_table by "wins" then by "totalPoints"

		record_table.sort( key=lambda k: (k[1],k[3]), reverse = True)
		col_names = ["Team","Wins","Losses","Points For"]
		row_names = list(range(1,(len(data)+1)))
		output = pandas.DataFrame(record_table,row_names,col_names)
		
		return output


	def calculateRecords(self,data):
		#return table of current records for every team
		#because I will do this same thing but potentially passing on positions
		#run through each matchup keep dictionary of team wins / losses
		records = {}
		#keys will be team numbers, values will be dictionary of "wins" and "losses"
		
		for matchup in data:
			#initialize records for team if just ran into them
			
			if matchup["homeTeamId"] not in records.keys():
				records[matchup["homeTeamId"]] = {"wins" : 0, "losses" : 0, "totalPoints" : 0}
			if matchup["awayTeamId"] not in records.keys():
				records[matchup["awayTeamId"]] = {"wins" : 0, "losses" : 0, "totalPoints" : 0}
		
			#calculate records
			if matchup["homeScore"] > matchup["awayScore"]:
				#win for home, loss for away
				records[matchup["homeTeamId"]]["wins"] += 1
				records[matchup["homeTeamId"]]["totalPoints"] += matchup["homeScore"]
				
				records[matchup["awayTeamId"]]["losses"] += 1
				records[matchup["awayTeamId"]]["totalPoints"] += matchup["awayScore"]
				
				
			elif matchup["homeScore"] < matchup["awayScore"]:
				#win for away, loss for home
				records[matchup["homeTeamId"]]["losses"] += 1
				records[matchup["homeTeamId"]]["totalPoints"] += matchup["homeScore"]
				
				records[matchup["awayTeamId"]]["wins"] += 1
				records[matchup["awayTeamId"]]["totalPoints"] += matchup["awayScore"]
				
			else:
				warnings.warn("Tie detected, not including this matchup in final standings")
				records[matchup["homeTeamId"]]["totalPoints"] += matchup["homeScore"]
				records[matchup["awayTeamId"]]["totalPoints"] += matchup["awayScore"]

		return records
		
		
	def adjustScore(self, data, position):
		#drop position from each team and recalculate scores
		#out_df = data
		#just going to edit in place.. think can do this here without changing 
		#outside script so don't need to duplicate

		loop_var = 0
		for matchup in data:
			score_home = self.sum_score(matchup["homeRoster"],position)
			score_away = self.sum_score(matchup["awayRoster"],position)
		
			#replace
			data[loop_var]["homeScore"] = score_home
			data[loop_var]["awayScore"] = score_away
			loop_var += 1
		
		return data
				
	
	def sum_score(self, data, position = "N/A"):
		#data will be a roster object from boxscore json
		#just returning a score because should be fed single roster
		#default NA for when called for regular score summing
		#wait, don't have to do this, eh keep for later anyway
		score = 0
		for player in data:
			if (player["position"] == "Bench") or (player["position"] == position):
				continue
			
			score += player["totalPoints"]
		
		return score
			
	def loadData(self, week_start, week_end, leagueID, year):
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
	
	
	
	
		
