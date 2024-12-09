#!/bin/python
#Alan E. Yocca
#09-17-20
#optimize_projection.py

import itertools
import pandas as pd
import argparse
import sys
#parser = argparse.ArgumentParser()
#parser.add_argument("--projections", required=True, help = "Projections file")
#parser.add_argument("--salary", required=True, help = "Salaries file")
#parser.add_argument("--include", required=False, help = "Comma separated list of teams to include")
#parser.add_argument("--exclude", required=False, help = "Comma separated list of teams to exclude")
#parser.add_argument("--max_iter", required=False, type = int, default = 9999999999, help = "max_iterations")
#parser.add_argument("--platform", required=False, default = "fanduel", help = "max_iterations")

#args = parser.parse_args()

def convert_dst(proj = dict()):
	#convert projection to salary defense names
	conv_dict = {"Los Angeles (LAR)" : "Los Angeles Rams",
				 "Buffalo (BUF)" : "Buffalo Bills",
				 "San Francisco (SF)" : "San Francisco 49ers",
				 "Pittsburgh (PIT)" : "Pittsburgh Steelers",
				 "Baltimore (BAL)" : "Baltimore Ravens",
				 "Kansas City (KC)" : "Kansas City Chiefs",
				 "Chicago (CHI)" : "Chicago Bears",
				 "Tennessee (TEN)" : "Tennessee Titans",
				 "New Orleans (NO)" : "New Orleans Saints",
				 "Tampa Bay (TB)" : "Tampa Bay Buccaneers",
				 "Philadelphia (PHI)" : "Philadelphia Eagles",
				 "Indianapolis (IND)" : "Indianapolis Colts",
				 "Arizona (ARI)" : "Arizona Cardinals",
				 "Seattle (SEA)" : "Seattle Seahawks",
				 "New England (NE)" : "New England Patriots",
				 "Green Bay (GB)" : "Green Bay Packers",
				 "Dallas (DAL)" : "Dallas Cowboys",
				 "Washington (WAS)" : "Washington Football Team",
				 "Minnesota (MIN)" : "Minnesota Vikings",
				 "Denver (DEN)" : "Denver Broncos",
				 "Cleveland (CLE)" : "Cleveland Browns",
				 "Cincinnati (CIN)" : "Cincinnati Bengals",
				 "Miami (MIA)" : "Miami Dolphins",
				 "New York (NYG)" : "New York Giants",
				 "Los Angeles (LAC)" : "Los Angeles Chargers",
				 "New York (NYJ)" : "New York Jets",
				 "Las Vegas (LV)" : "Las Vegas Raiders",
				 "Detroit (DET)" : "Detroit Lions",
				 "Jacksonville (JAC)" : "Jacksonville Jaguars",
				 "Atlanta (ATL)" : "Atlanta Falcons",
				 "Carolina (CAR)" : "Carolina Panthers",
				 "Houston (HOU)" : "Houston Texans"}
	
	for team in conv_dict.keys():
		proj = proj.replace(team, conv_dict[team])
	return proj


#going to have one master list,
#compute all possible combinations using indicies
#dive into weights of index combination
#compute score
#keep it max
#skip if over budget
#how to avoid computing subproblems? Might not be worth it, might be good as is....

def optimize_projection(projections = '', salary = '', max_iter = 30000000, platform = '', include = '', exclude = ''):
    #where should these import statements come from...
    import itertools
    import pandas as pd
    import argparse
    import sys
    import datetime

    print("Loading projections / salaries")
    projections_df = pd.read_csv(projections)
    salary_df = pd.read_csv(salary)

    #defense naming not consistent between these
    projections_df = convert_dst(proj = projections_df)

    #filter for slate
    #default slate just a check for all Sunday games
    salary_df = salary_df[salary_df['Kickoff'].str.startswith("Sun")]
    
    #combine
    result = pd.merge(projections_df, salary_df, on = "Name")

    #include / exclude
    if (include != ''):
        include_list = include.split(",")
        result = result[result['Team_x'].isin(include_list)]
    if (exclude != ''):
        exclude_list = exclude.split(",")
        result = result[~result['Team_x'].isin(exclude_list)]

    #create new column (v/w)
    result["Value"] = result["Projection"]/result["Salary"]

    #sort
    sorted = result.sort_values(by=["Value"], ascending = False)

    #select the top 10!
    master_names = []
    master_weights = []
    master_scores = []

    #append qbs. Position_x cuz something got messed up maybe? First glance, this column seems correct
    master_names = master_names + list(sorted[sorted['Position_y'].str.match('QB')]['Name'])[0:10]
    master_weights = master_weights + list(sorted[sorted['Position_y'].str.match('QB')]['Salary'])[0:10]
    master_scores = master_scores + list(sorted[sorted['Position_y'].str.match('QB')]['Projection'])[0:10]

    #append rbs
    master_names = master_names + list(sorted[sorted['Position_y'].str.match('RB')]['Name'])[0:10]
    master_weights = master_weights + list(sorted[sorted['Position_y'].str.match('RB')]['Salary'])[0:10]
    master_scores = master_scores + list(sorted[sorted['Position_y'].str.match('RB')]['Projection'])[0:10]

    #append wrs
    master_names = master_names + list(sorted[sorted['Position_y'].str.match('WR')]['Name'])[0:10]
    master_weights = master_weights + list(sorted[sorted['Position_y'].str.match('WR')]['Salary'])[0:10]
    master_scores = master_scores + list(sorted[sorted['Position_y'].str.match('WR')]['Projection'])[0:10]

    #append te
    master_names = master_names + list(sorted[sorted['Position_y'].str.match('TE')]['Name'])[0:10]
    master_weights = master_weights + list(sorted[sorted['Position_y'].str.match('TE')]['Salary'])[0:10]
    master_scores = master_scores + list(sorted[sorted['Position_y'].str.match('TE')]['Projection'])[0:10]

    #append defense
    master_names = master_names + list(sorted[sorted['Position_y'].str.match('DF')]['Name'])[0:10]
    master_weights = master_weights + list(sorted[sorted['Position_y'].str.match('DF')]['Salary'])[0:10]
    master_scores = master_scores + list(sorted[sorted['Position_y'].str.match('DF')]['Projection'])[0:10]

    qb_index = list(range(0,10))
    rb_index = list(range(10,20))
    wr_index = list(range(20,30))
    te_index = list(range(30,40))
    op_index = list(range(10,40))
    df_index = list(range(40,50))

    #selecting multiple
    rbs = list(itertools.combinations(rb_index,2))
    wrs = list(itertools.combinations(wr_index,3))

    full_list = [qb_index, rbs, wrs, te_index, op_index, df_index]

    print("Calculating combinations")
    combinations = [p for p in itertools.product(*full_list)]

    #yea there aren't enough combinations for me to be worried about it

    max_score = 0
    if platform == "fanduel":
        max_weight = 60000
    elif platform == "draftkings":
        max_weight = 50000
    else:
        sys.exit("Specify fanduel or draftkings for keyword platform")
    max_lineup_idx = []

    print("Assessing combinations")

    for i in range(0,len(combinations)):
        if i > max_iter:
            break
        if i % 10000000 == 0:
            print("Through %s lineups" % (i))
            print("Current max projection: %s" % (max_score))

        comb = combinations[i]
        idx_list = []
        for item in comb:
            if isinstance(item, tuple):
                for sub_item in item:
                    idx_list.append(sub_item)
            else:
                idx_list.append(item)
        
        #skip if player listed more than once
        if len(idx_list) > len(set(idx_list)):
            continue

        #calculate weight
        try:
            weight = [master_weights[x] for x in idx_list]
        except IndexError:
            print(master_weights)
            sys.exit(idx_list)
        
        if sum(weight) > max_weight:
            continue
        
        #calculate score
        score = [master_scores[x] for x in idx_list]
        
        if sum(score) > max_score:
            max_score = sum(score)
            max_lineup_idx = idx_list

    #print out best found lineup
    print("Optimal lineup for %s" % (platform))
    data = {"Player" : [master_names[x] for x in max_lineup_idx] + ["Total:"],
            "Price" : [master_weights[x] for x in max_lineup_idx] + [sum([master_weights[x] for x in max_lineup_idx])],
            "Prediction" : [master_scores[x] for x in max_lineup_idx] + [sum([master_scores[x] for x in max_lineup_idx])]}

    df = pd.DataFrame (data, columns = ['Player','Price','Prediction'])

    print(df)
    
    #save df to file for posterity.. 
    #lineups/platform'datestring.txt
    date_string = str(datetime.date.today())
    out_filename = "lineups/" + platform + "_" + date_string + ".csv"
    df.to_csv(out_filename, index = False)

    print("Finished")









