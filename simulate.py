import itertools
import random
import numpy as np


# Runs the simulation with the provided arguments
def simulate_old(playerList, totalSteps, rate, matchSize, verbose):
    random.seed()
    if (verbose and totalSteps > 0):
        print('Running for max # steps', totalSteps)
    elif (verbose):
        print('Running until all players matched, or not enough left to make a match')
    matches = []
    queue = []
    queueLenAtTimeT = []
    t = 1
    while (totalSteps == 0 or t <= totalSteps):
        queueLenAtTimeT.append(len(queue))
        endTime = t
        # Decide whether a player joins the queue at time t
        if (len(playerList) > 0 and random.random() < rate):
            player = {'timeAdded': t, 'skill': playerList.pop(random.randrange(len(playerList)))}
            if (verbose): print('Player joined queue', player)
            queue.append(player)

        # Check for matches, make them as needed
        if (len(queue) >= matchSize):
            matching = matchmake1(queue, t, matchSize)
            queue = matching['queue']
            matches.extend(matching['matches'])

        if (len(playerList) == 0 and len(queue) < matchSize):
            break
        t += 1

    if (verbose): print('Done matching, ran through time', t)

    # Calculate results
    matchResults = []
    for match in matches:
        skillList = list(map((lambda x: x['skill']), match['players']))
        meanSkill = np.mean(skillList)
        varSkill = np.var(skillList)
        stdSkill = np.std(skillList)
        minSkill = min(skillList)
        maxSkill = max(skillList)
        gapSkill = maxSkill - minSkill
        skillStats = {'list': skillList, 'mean': meanSkill, 'var': varSkill, 'stddev': stdSkill, 'min': minSkill,
                      'max': maxSkill, 'gap': gapSkill}
        # Measure time between joining the queue and being matched
        timeList = list(map((lambda x: match['timeCreated'] - x['timeAdded']), match['players']))
        meanTime = np.mean(timeList)
        varTime = np.var(timeList)
        stdTime = np.std(timeList)
        minTime = min(timeList)
        maxTime = max(timeList)
        gapTime = maxTime - minTime
        timeStats = {'list': timeList, 'mean': meanTime, 'var': varTime, 'stddev': stdTime, 'min': minTime,
                     'max': maxTime, 'gap': gapTime}
        result = {'skills': skillStats, 'times': timeStats}
        matchResults.append(result)

    result = {'matchResults': matchResults, 'queue': queue, 'queueLenAtTimeT': queueLenAtTimeT}
    return result


# Matchmaking algorithms
# Return in the form { queue, matches }

# First come first serve, disregard skill
def matchmake1(queue, currentTime, matchSize, matchAccumulator=[]):
    group = queue[0:5]
    newQueue = [x for x in queue if x not in group]
    matchAccumulator.append({'players': group, 'timeCreated': currentTime})
    return {'queue': newQueue, 'matches': matchAccumulator}


# Greedily choose the first combination with low std. deviation
def matchmake2(queue, currentTime, matchSize, matchAccumulator=[]):
    allCombinations = itertools.combinations(queue, matchSize)
    for group in allCombinations:
        skillList = list(map((lambda x: x['skill']), group))
        mean = np.mean(skillList)
        stddev = np.std(skillList)
        if (stddev <= (mean / 10)):
            # Found a match, greedily use the first
            newQueue = [x for x in queue if x not in group]
            matchAccumulator.append({'players': group, 'timeCreated': currentTime})
            return matchmake1(newQueue, currentTime, matchSize, matchAccumulator)
    return {'queue': queue, 'matches': matchAccumulator}


# Runs the simulation and returns a map of statistics to values
def simulate(players, iterations, match_size):
    for x in range(iterations):
        matches = random_matchmake(players, match_size)

        for match in matches:
            sim_match(match[0], match[1])


	abs_delta_list = []
	for player in players:
		abs_delta_list.append(abs(player.true_skill - player.est_skill))

	data_map = {'size': len(abs_delta_list),
				'mean': np.mean(abs_delta_list),
				'median': np.median(abs_delta_list),
				'variance': np.var(abs_delta_list),
				'standard deviation': np.std(abs_delta_list),
				'minimum': np.min(abs_delta_list),
				'maximum': np.max(abs_delta_list)}

	return {'players': players, 'skill level difference stats': data_map}


# Creates an array of matches of the given size by randomly assigning players to matches
def random_matchmake(players, match_size):
    temp_players = list(players)
    random.shuffle(temp_players)
    matches_to_fill = len(temp_players) / match_size
    matches = []
    while matches_to_fill > 0:
        team_a = []
        team_a_slots = match_size / 2
        team_b = []
        team_b_slots = match_size - team_a_slots
        while team_a_slots > 0:
            next_player = temp_players.pop(0)
            team_a.append(next_player)
            team_a_slots -= 1
        while team_b_slots > 0:
            next_player = temp_players.pop(0)
            team_b.append(next_player)
            team_b_slots -= 1
        matches.append((team_a, team_b))
        matches_to_fill -= 1

    return matches


# Simulates a match between two teams and adjusts their players' Elo rankings accordingly
def sim_match(team_a, team_b):
    team_a_true_avg = 0
    team_a_est_avg = 0
    a_size = len(team_a)
    for player in team_a:
        team_a_true_avg += player.true_skill
        team_a_est_avg += player.est_skill
    team_a_true_avg /= a_size
    team_a_est_avg /= a_size

    team_b_true_avg = 0
    team_b_est_avg = 0
    b_size = len(team_b)
    for player in team_b:
        team_b_true_avg += player.true_skill
        team_b_est_avg += player.est_skill
    team_b_true_avg /= b_size
    team_b_est_avg /= b_size

    a_wins = match_outcome(team_a_true_avg, team_b_true_avg)

    if a_wins:
        a_delta = estimated_elo_change(team_a_est_avg, team_b_est_avg)
        b_delta = -1 * a_delta
    else:
        b_delta = estimated_elo_change(team_b_est_avg, team_a_est_avg)
        a_delta = -1 * b_delta

    for player in team_a:
        player.est_skill += a_delta

    for player in team_b:
        player.est_skill += b_delta


# Returns true if the holder of the first Elo value wins and false otherwise
def match_outcome(elo1, elo2):
    return random.uniform(0, 1) < elo_probability(elo1, elo2)


# Returns the expected probability of the holder of the first Elo rating winning
def elo_probability(elo1, elo2):
    return 1.0 / (1.0 + pow(10, (elo2 - elo1) / 400))


# Returns how many points are added to the winner's Elo ranking
def estimated_elo_change(winning_elo, losing_elo):
    winning_prob = elo_probability(winning_elo, losing_elo)
    return 32.0 * (1.0 - winning_prob)
