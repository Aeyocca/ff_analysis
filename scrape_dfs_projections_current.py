#!/bin/python
#Alan E. Yocca
#09-18-20
#scrape_dfs_projections_current.py

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sys
import datetime
import re
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--full_ppr", required=False, default = 0, help = "if set to 1, then full ppr (DK), else half ppr (fanduel)")


args = parser.parse_args()

#https://www.fantasypros.com/nfl/rankings/qb.php

#automate this please
date_string = str(datetime.date.today())

url="https://www.fantasypros.com/nfl/rankings/qb.php"
response = requests.get(url)
soup = bs(response.content, 'lxml')
rawJ = soup.find_all('script', type = 'text/javascript')
#>>> len(rawJ)
#44
#if 44, then rawJ[29]
J = str(rawJ[29])
#if 51, then rawJ[37]
jidx = 37
J = str(rawJ[jidx])
J1 = J.split('var ecrData = ')
J2 = J1[1].rsplit('var sosData =')
J3 = J2[0].rsplit(';', 1)
JsonText = J3[0]
s = json.loads(JsonText)

all_name = []
all_pos = []
all_proj = []
all_team = []
erroneous_entry = 0

for player in s['players']:
	try:
		all_name.append(player['player_name'])
		all_pos.append("QB")
		#if no projection, add zero
		all_proj.append(player.get('r2p_pts', 0))		
		all_team.append(player['player_team_id'])
	except:
		erroneous_entry += 1
		#sys.exit("Failed to extract info from this object: %s" % (player))

if args.full_ppr:
    url="https://www.fantasypros.com/nfl/rankings/ppr-rb.php"
else:
    url="https://www.fantasypros.com/nfl/rankings/half-point-ppr-rb.php"

response = requests.get(url)
soup = bs(response.content, 'lxml')
rawJ = soup.find_all('script', type = 'text/javascript')
#J = str(rawJ[29])
J = str(rawJ[jidx])
J1 = J.split('var ecrData = ')
J2 = J1[1].rsplit('var sosData =')
J3 = J2[0].rsplit(';', 1)
JsonText = J3[0]
s = json.loads(JsonText)

for player in s['players']:
	try:
		all_name.append(player['player_name'])
		all_pos.append("RB")
		#if no projection, add zero
		all_proj.append(player.get('r2p_pts', 0))		
		all_team.append(player['player_team_id'])
	except:
		erroneous_entry += 1
		#sys.exit("Failed to extract info from this object: %s" % (player))

if args.full_ppr:
    url="https://www.fantasypros.com/nfl/rankings/ppr-wr.php"
else:
    url="https://www.fantasypros.com/nfl/rankings/half-point-ppr-wr.php"

response = requests.get(url)
soup = bs(response.content, 'lxml')
rawJ = soup.find_all('script', type = 'text/javascript')
#J = str(rawJ[29])
J = str(rawJ[jidx])
J1 = J.split('var ecrData = ')
J2 = J1[1].rsplit('var sosData =')
J3 = J2[0].rsplit(';', 1)
JsonText = J3[0]
s = json.loads(JsonText)

for player in s['players']:
	try:
		all_name.append(player['player_name'])
		all_pos.append("WR")
		#if no projection, add zero
		all_proj.append(player.get('r2p_pts', 0))		
		all_team.append(player['player_team_id'])
	except:
		erroneous_entry += 1
		#sys.exit("Failed to extract info from this object: %s" % (player))

if args.full_ppr:
    url="https://www.fantasypros.com/nfl/rankings/ppr-te.php"
else:
    url="https://www.fantasypros.com/nfl/rankings/half-point-ppr-te.php"

response = requests.get(url)
soup = bs(response.content, 'lxml')
rawJ = soup.find_all('script', type = 'text/javascript')
#J = str(rawJ[29])
J = str(rawJ[jidx])
J1 = J.split('var ecrData = ')
J2 = J1[1].rsplit('var sosData =')
J3 = J2[0].rsplit(';', 1)
JsonText = J3[0]
s = json.loads(JsonText)

for player in s['players']:
	try:
		all_name.append(player['player_name'])
		all_pos.append("TE")
		#if no projection, add zero
		all_proj.append(player.get('r2p_pts', 0))		
		all_team.append(player['player_team_id'])
	except:
		erroneous_entry += 1
		#sys.exit("Failed to extract info from this object: %s" % (player))

url="https://www.fantasypros.com/nfl/rankings/dst.php"
response = requests.get(url)
soup = bs(response.content, 'lxml')
rawJ = soup.find_all('script', type = 'text/javascript')
#J = str(rawJ[29])
J = str(rawJ[jidx])
J1 = J.split('var ecrData = ')
J2 = J1[1].rsplit('var sosData =')
J3 = J2[0].rsplit(';', 1)
JsonText = J3[0]
s = json.loads(JsonText)

for player in s['players']:
	try:
		all_name.append(player['player_name'])
		all_pos.append("DF")
		#if no projection, add zero
		all_proj.append(player.get('r2p_pts', 0))		
		all_team.append(player['player_team_id'])
	except:
		erroneous_entry += 1
		#sys.exit("Failed to extract info from this object: %s" % (player))

print(erroneous_entry)
data = {"Name" : all_name,
		"Position" : all_pos,
		"Projection" : all_proj,
		"Team" : all_team}

df = pd.DataFrame (data, columns = ['Name','Position','Projection','Team'])

if args.full_ppr:
    out_filename = "projections/fantasypro_dfs_proj_fullppr" + date_string + ".csv"
else:
    out_filename = "projections/fantasypro_dfs_proj_halfppr" + date_string + ".csv"
df.to_csv(out_filename, index = False)



