import myFunc from "./hello.mjs";
import node from '/Users/alanyocca/Documents/ff_19/npm/node_modules/espn-fantasy-football-api/node.js'; // node
import lodash from '/Users/alanyocca/Documents/ff_19/npm//node_modules/lodash/lodash.js';
import json from '/usr/local/lib/node_modules/json/lib/json.js';

const { Client } = node;
const { _ } = lodash;

//myFunc();


// const { Client } = require('espn-fantasy-football-api/node'); // node
// import { Client } from '/Users/alanyocca/Documents/ff_19/npm/node_modules/espn-fantasy-football-api/node'; // node

// SWID: {579DBFEA-32EA-4837-9D10-18E6702BC578}
// SWID: {579DBFEA-32EA-4837-9D10-18E6702BC578}
// espn_s2: AEBvGnceGhmW%2BEy7DCEloPq%2BO7v3%2B8lSKke85iKNP5mI2SouKXmH2c32FA%2Fbt8ICZJua4imYmTgcIEWSD6yS3XlJ2dNBrpKHJlG408OLJI1jJ87khIy91g%2FDjCml5WjFhyJxeZP469kBfTpQ4ZJH%2B1xDwlLR51x5Fy%2BVG33Eli%2BiKNO6vqzgZxJKsKJmeAvPQKpd%2BPNqeV1qTr8KRaTW74BSPiNlyB%2BzAmifg3RY3zvD7kBDmbErxselA4cZKAkfb24%3D

const myClient = new Client({ leagueId: 592833 });

// example league 387659
// const myClient = new Client({ leagueId: 387659 });

myClient.setCookies({ 
	espnS2: 'AEBvGnceGhmW%2BEy7DCEloPq%2BO7v3%2B8lSKke85iKNP5mI2SouKXmH2c32FA%2Fbt8ICZJua4imYmTgcIEWSD6yS3XlJ2dNBrpKHJlG408OLJI1jJ87khIy91g%2FDjCml5WjFhyJxeZP469kBfTpQ4ZJH%2B1xDwlLR51x5Fy%2BVG33Eli%2BiKNO6vqzgZxJKsKJmeAvPQKpd%2BPNqeV1qTr8KRaTW74BSPiNlyB%2BzAmifg3RY3zvD7kBDmbErxselA4cZKAkfb24%3D', 
	SWID: '{579DBFEA-32EA-4837-9D10-18E6702BC578}' 
});

class Psychic {
  static filterPosition(boxscorePlayer, position) {
    return (
      boxscorePlayer.position === position ||
      _.includes(boxscorePlayer.player.eligiblePositions, position)
    );
  }

  static handleNonFlexPosition(lineup, position) {
    const players = _.filter(lineup, (player) => this.filterPosition(player, position));
    const sortedPlayers = _.sortBy(players, ['totalPoints']);
    return _.last(sortedPlayers);
  }

  static analyzeLineup(lineup, score) {
    let bestSum = 0;
    const bestRoster = [];
    let numChanges = 0;

    const bestQB = this.handleNonFlexPosition(lineup, 'QB')
    bestRoster.push(bestQB.player.fullName);
    bestSum += bestQB.totalPoints;
    if (bestQB.position === 'Bench') {
      numChanges += 1;
    }

    const bestDefense = this.handleNonFlexPosition(lineup, 'D/ST')
    bestRoster.push(bestDefense.player.fullName);
    bestSum += bestDefense.totalPoints;
    if (bestDefense.position === 'Bench') {
      numChanges += 1;
    }

    const bestKicker = this.handleNonFlexPosition(lineup, 'K')
    bestRoster.push(bestKicker.player.fullName);
    bestSum += bestKicker.totalPoints;
    if (bestKicker.position === 'Bench') {
      numChanges += 1;
    }


    const flexPlayers = _.filter(lineup, (player) => this.filterPosition(player, 'RB') ||
      this.filterPosition(player, 'WR') ||
      this.filterPosition(player, 'TE')
    );
    const sortedFlexPlayers = _.sortBy(flexPlayers, ['totalPoints']);

    const flexPos = { RB: 2, WR: 2, TE: 1, FLEX: 1 };

    while (_.sum(_.values(flexPos)) && !_.isEmpty(sortedFlexPlayers)) {
      const player = sortedFlexPlayers.pop();
      const acceptPlayer = () => {
        bestRoster.push(player.player.fullName);
        bestSum += player.totalPoints;
        if (player.position === 'Bench') {
          numChanges += 1;
        }
      }

      if (flexPos.RB && _.includes(player.player.eligiblePositions, 'RB')) {
        acceptPlayer();
        flexPos.RB -= 1;
      } else if (flexPos.WR && _.includes(player.player.eligiblePositions, 'WR')) {
        acceptPlayer();
        flexPos.WR -= 1;
      } else if (flexPos.TE && _.includes(player.player.eligiblePositions, 'TE')) {
        acceptPlayer();
        flexPos.TE -= 1;
      } else if (flexPos.FLEX) {
        acceptPlayer();
        flexPos.FLEX -= 1;
      }
    }

    return {
      bestSum,
      bestRoster,
      currentScore: score,
      numChanges
    };
  }

  static runForWeek({ seasonId, matchupPeriodId, scoringPeriodId }) {
    const bestLineups = {};
    return myClient.getBoxscoreForWeek({ seasonId, matchupPeriodId, scoringPeriodId }).then((boxes) => {
      _.forEach(boxes, (box) => {
        bestLineups[box.awayTeamId] = this.analyzeLineup(box.awayRoster, box.awayScore);
        bestLineups[box.homeTeamId] = this.analyzeLineup(box.homeRoster, box.homeScore);
      });

      return bestLineups;
    });
  }
}

//Psychic.runForWeek({ seasonId: 2019, matchupPeriodId: 1, scoringPeriodId: 1 }).then((result) => {
//  console.log(result);
// return result;
//});

//	console.log(myClient.getBoxscoreForWeek({ seasonId, matchupPeriodId, scoringPeriodId })

//class tmp_stuff {
//  static load_data() {
//  
//  }
//}

//tmp_stuff.load_data

//myClient.getBoxscoreForWeek({ seasonId: 2019, matchupPeriodId: 1, scoringPeriodId: 1 }).then((result) => {
//	_.forEach(boxes, (box) => {
//		console.log(box.awayScore);
//		//return result;
//	})
//});

var matchupPID = parseInt((process.argv[3]))
var scoringPID = parseInt((process.argv[4]))

myClient.getBoxscoreForWeek({ seasonId: (process.argv[2]), matchupPeriodId: matchupPID, scoringPeriodId: scoringPID }).then((result) => {
//	_.forEach(box_scores, (result) => {
//		console.log(box.awayScore)
//	})
	
	console.log(JSON.stringify(result, null, 4));
//	console.log(result[0]);
//	return result;
});

//console.log(JSON.stringify(myObject, null, 4));


//console.log(tmp.toString());
//console.log(Object.keys(tmp));

//for (let j = 0; j < process.argv.length; j++) {
//    console.log(j + ' -> ' + (process.argv[j]));
//}
