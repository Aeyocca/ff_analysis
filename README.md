\# ff_analysis
### 11-05-19
## Fantasy football analysis for the Boyz fantasy football league
First release, add classes as you see fit

## Quick installation:
tradeAnalyzer only class currently, but will be rearranging / adding things over time

1.) Download this repo as a zip file

2.) Unzip and move into this directory:

`$ unzip ff_analysis-master.zip && cd ff_analysis-master`

3.) Create your own control file to specify players involved in trade and weeks interested in
- Eventually will allow specification on cmd line or file easier to edit than json format

`$ cp test/test_ctl_file.json ./myTrade_ctl_file.json`
- edit parameters in here, pretty self explanatory

4.) Analyze your trade!
`$ python trade_analyzer.py myTrade_ctl_file.json`
- This should output a nicely (hopefully) formatted table comparing the trade


## more details
- boxscores come from javascript I found on the internet, will add to this module eventually so you don't have to come back here everyweek for updated boxscores
- class tradeAnalyzer is the only one but I will split that up to use some of its methods (which aren't super portable...) for other functions
- boxscores files are just json meta information from scoreboards, therefore no player data is available for players in weeks they were not rostered
- also does NOT check for which team they scored points for through the time period specified
-- ie if you dropped a player and someone else picked them up, points scored for someone else will be included in the output table

## functionalities I plan to add
- cmd line arguments to override ctl json parameters to be more user-friendly / faster
- find what makes this so damn slow, think it might be loading large modules
- factor in which team these players were on to control for players traded away during the period you are interested in
- calculating points obtained from certain roster spots (ie how many points did I get from kickers this season??)
- translate team numbers into team names to print to output instead of "team 1" and "team 2"
- enter trade date to automatically calculate the week since that can be hard to look up

Please share if you want something / will add it yourself


# Package requirements:
- json
- sys
- re
- pandas
- numpy

All should come with standard python distros.
