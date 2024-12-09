#12-01-24
#sunday_DFS_NFL.py
#full pipeline to scrape and optimize fanduel and draftkings

#still get to set single platform if thats all we want
#as well as max_iterations, found 30million is more than enough 
#90% of the time we get optimum at first 10 million

import argparse
import sys
from DFS_NFL import scrapeProjections
from DFS_NFL import scrapeSalary
from DFS_NFL import optimize
parser = argparse.ArgumentParser()
parser.add_argument("--include", required=False, help = "Comma separated list of teams to include")
parser.add_argument("--exclude", required=False, help = "Comma separated list of teams to exclude")
parser.add_argument("--max_iter", required=False, type = int, default = 30000000, help = "max_iterations")
parser.add_argument("--platform", required=False, default = "fanduel", help = "max_iterations")

args = parser.parse_args()

full_ppr_projections = scrapeProjections.scrape_dfs_projections(full_ppr = True)
half_ppr_projections = scrapeProjections.scrape_dfs_projections(full_ppr = False)

fanduel_salaries = scrapeSalary.scrape_dfs_salaries(platform = "fanduel")
draftkings_salaries = scrapeSalary.scrape_dfs_salaries(platform = "draftkings")

#calling optimize, print to screen and save to file

optimize.optimize_projection(projections = half_ppr_projections, 
    salary = fanduel_salaries, max_iter = 30000000, platform = 'fanduel')

optimize.optimize_projection(projections = full_ppr_projections, 
    salary = draftkings_salaries, max_iter = 30000000, platform = 'draftkings')
