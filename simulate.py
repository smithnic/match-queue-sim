import itertools
import random
import numpy as np

# Runs the simulation with the provided arguments
def simulate(playerList, totalSteps, rate, matchSize, verbose):
	random.seed()
	if (verbose and totalSteps > 0): print('Running for max # steps', totalSteps)
	elif (verbose): print('Running until all players matched, or not enough left to make a match')
	matches = []
	queue = []
	queueLenAtTimeT = []
	t = 1
	while (totalSteps == 0 or t <= totalSteps):
		queueLenAtTimeT.append(len(queue))
		endTime = t
		# Decide whether a player joins the queue at time t
		if (len(playerList) > 0 and random.random() < rate):
			player = { 'timeAdded': t, 'skill': playerList.pop(random.randrange(len(playerList))) }
			if (verbose): print('Player joined queue', player)
			queue.append(player)
		
		# Check for matches, make them as needed
		if (len(queue) >= matchSize):
			matching = matchmake1(queue, t, matchSize)
			queue = matching['queue']
			matches.extend(matching['matches'])
		
		if (len(playerList) == 0 and len(queue) < matchSize):
			break
		t+=1

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
		skillStats = { 'list': skillList, 'mean': meanSkill, 'var': varSkill, 'stddev': stdSkill, 'min': minSkill, 'max': maxSkill, 'gap': gapSkill }
		# Measure time between joining the queue and being matched
		timeList = list(map((lambda x: match['timeCreated'] - x['timeAdded']), match['players']))
		meanTime = np.mean(timeList)
		varTime = np.var(timeList)
		stdTime = np.std(timeList)
		minTime = min(timeList)
		maxTime = max(timeList)
		gapTime = maxTime - minTime
		timeStats = { 'list': timeList, 'mean': meanTime, 'var': varTime, 'stddev': stdTime, 'min': minTime, 'max': maxTime, 'gap': gapTime }
		result = { 'skills': skillStats, 'times': timeStats }	
		matchResults.append(result)

	result = { 'matchResults': matchResults, 'queue': queue, 'queueLenAtTimeT': queueLenAtTimeT }
	return result

# Matchmaking algorithms
# Return in the form { queue, matches }

# First come first serve, disregard skill
def matchmake1(queue, currentTime, matchSize, matchAccumulator=[]):
	group = queue[0:5]
	newQueue = [x for x in queue if x not in group]
	matchAccumulator.append({ 'players': group, 'timeCreated': currentTime })
	return { 'queue': newQueue, 'matches': matchAccumulator }

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
			matchAccumulator.append({ 'players': group, 'timeCreated': currentTime })
			return matchmake1(newQueue, currentTime, matchSize, matchAccumulator)
	return { 'queue': queue, 'matches': matchAccumulator }
