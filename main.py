import argparse
from simulate import simulate

# Players are represented by a number which is the value for their skill/"ELO"
# To simulate continuous time, increase amount of steps and decrease the rate players are introduced

''' TODO
- Generate a pool of players of a given size
	- Must provide minimum skill rating, maximum skill rating and generate normal distribution
'''
parser = argparse.ArgumentParser(description='Simulate a matchmaking scenario')

# To simulate continuous time, increase amount of steps and decrease the rate players are introduced

parser.add_argument('totalSteps', metavar='totalSteps', type=int, help='The total time to run the simulation')

parser.add_argument('rate', metavar='rate', type=float, help='A Value between 0 and 1 representing probability of a player being introduced in one step')

parser.add_argument('matchSize', metavar='matchSize', type=int, help='Number of players which forms a match')

parser.add_argument('--playersFile', dest='playersFile', metavar='filePath', type=argparse.FileType('r'), required=False)

args = parser.parse_args()

# Argument validation
if (args.totalSteps <= 0):
	print('totalSteps must be positive')
	quit()

if (args.rate <= 0 or args.rate >= 1):
	print('rate must be between 0 and 1 exclusive')
	quit()

if (args.matchSize <= 0):
	print('matchSize must be positive')
	quit()

if (not args.playersFile):
	print('Not using playersFile, generating players')
	# TODO use numpy to generate a normal distribution of players
else:
	print('Using provided playersFile')
	with args.playersFile as playersFile:
		# Split the file by whitespace to convert into list of integers
		players = list(map(int, playersFile.read().split()))

# Execute the simulation
result = simulate(players, args.totalSteps, args.rate, args.matchSize)
print(result)

print('done')
