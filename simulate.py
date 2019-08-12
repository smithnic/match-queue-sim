import random
import numpy as np

# Runs the simulation with the provided arguments
# TODO probably other args
def simulate(playerList, totalSteps, rate, matchSize):
	random.seed()
	print('Making matches of size', matchSize, ', running for # steps', totalSteps)
	matches = []
	queue = []
	for t in range(1, totalSteps):
		if (len(playerList) == 0):
			print('Finished early at time ', t)
			break
		# Decide whether a player joins the queue at time t
		if (random.random() < rate):
			player = {'timeAdded': t, 'skill': playerList.pop(random.randrange(len(playerList)))}
			queue.append(player)
		
		# Check for matches, make them as needed
		# TODO
	
	# Print results
	matchResults = []
	for match in matches:
		skillList = list(map((lambda x: x.skill), match))
		meanSkill = np.mean(skillList)
		varSkill = np.var(skillList)
		minSkill = min(skillList)
		maxSkill = max(skillList)
		skillGap = maxSkill - minSkill
		result = { skillList, meanSkill, varSkill, minSkill, maxSkill, skillGap }
		matchResults.push(result)
	
	result = { 'matchResults': matchResults, 'queue': queue }
	return result

