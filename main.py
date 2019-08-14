import argparse
import pprint
from simulate import simulate

# Players are represented by a number which is the value for their skill/"ELO"
# To simulate continuous time, increase amount of steps and decrease the rate players are introduced

''' TODO
- Give players some 'ID' Value
- Run matchmaking multiple times
'''
parser = argparse.ArgumentParser(description='Simulate a matchmaking scenario')

parser.add_argument('rate', metavar='rate', type=float, help='A Value between 0 and 1 representing probability of a player being introduced in one step')

parser.add_argument('matchSize', metavar='matchSize', type=int, help='Number of players which forms a match')

parser.add_argument('playersFile', metavar='filePath', type=argparse.FileType('r'))

parser.add_argument('--totalSteps', dest='totalSteps', metavar='totalSteps', type=int, help='The total time to run the simulation, otherwise runs until player list exhausted')

parser.add_argument('-v', action='store_true', help='Enable verbose output')

args = parser.parse_args()

# Argument validation
if (args.totalSteps):
	if (args.totalSteps <= 0):
		print('totalSteps must be positive')
		quit()
	totalSteps = args.totalSteps
else:
	# Internally use 0 to signify run until list is exhausted
	totalSteps = 0

if (args.rate <= 0 or args.rate >= 1):
	print('rate must be between 0 and 1 exclusive')
	quit()

if (args.matchSize <= 0):
	print('matchSize must be positive')
	quit()

with args.playersFile as playersFile:
	# Split the file by whitespace to convert into list of integers
	players = list(map(int, playersFile.read().split()))

# Execute the matchmaking simulation
result = simulate(players, totalSteps, args.rate, args.matchSize, args.v)

# Print results
pp = pprint.PrettyPrinter(indent=1)
pp.pprint(result['matchResults'])
