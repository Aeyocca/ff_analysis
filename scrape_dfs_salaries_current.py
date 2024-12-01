#!/bin/python
#Alan E. Yocca
#09-18-20
#scrape_dfs_salaries_current.py

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sys
import datetime
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--platform", required=False, default = "fanduel", help = "fanduel or draftkings")


args = parser.parse_args()
#https://www.fantasypros.com/daily-fantasy/nfl/fanduel-salary-changes.php

#automate this please
date_string = str(datetime.date.today())

if args.platform == "fanduel":
    url="https://www.fantasypros.com/daily-fantasy/nfl/fanduel-salary-changes.php"
elif args.platform == "draftkings":
    url="https://www.fantasypros.com/daily-fantasy/nfl/draftkings-salary-changes.php"
else:
    sys.exit("Select one of fanduel or draftkings for --platform")

response = requests.get(url)
soup = bs(response.content, 'lxml')

#whats my output going to look like?

#Name	Pos	Price

#all_games = soup.find_all('td', class_='sportPicksBorder')
player_table = soup.find_all('div', class_='mobile-table')


qb = player_table[0].find_all('tr', class_='QB')

#name = qb[0].find_all('a')[0].get_text()
#salary = qb[0].find('td', class_='salary').get('data-salary')

rb = player_table[0].find_all('tr', class_='RB')

wr = player_table[0].find_all('tr', class_='WR')

te = player_table[0].find_all('tr', class_='TE')

df = player_table[0].find_all('tr', class_='DST')

all_name = []
all_pos = []
all_salary = []
all_team = []
data_list = [qb,   rb,   wr,   te,   df]
pos_list = ["QB", "RB", "WR", "TE", "DF"]
for pos in range(0,len(pos_list)):
	for player in data_list[pos]:
		try:
			name = player.find_all('a')[0].get_text()
			salary = player.find('td', class_='salary').get('data-salary')
			kickoff = player.find('td', class_='ko').get_text()
			team_pos_string = player.find('small').get_text()
			p_string = team_pos_string[team_pos_string.find("(")+1:team_pos_string.rfind(")")]
			team = p_string.split(' - ')[0]
		except:
			sys.exit("Failed extracting info from this object: %s" % (player))
		
		if name == "A.J. Green" and pos_list[pos] == "TE":
			print("skipping the bastard Browns TE AJ Green")
			continue
		
		#skip games not in main slate
		if not kickoff.startswith("Sun") or kickoff.endswith("8:20PM"):
			continue
		all_name.append(name)
		all_pos.append(pos_list[pos])
		all_salary.append(salary)
		all_team.append(team)


data = {"Name" : all_name,
		"Position" : all_pos,
		"Salary" : all_salary,
		"Team" : all_team}

df = pd.DataFrame (data, columns = ['Name','Position','Salary','Team'])
df.to_csv("salary/" + args.platform + "_dfs_salary_" + date_string + ".csv", index = False)


