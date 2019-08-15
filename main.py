import argparse
import pprint
from simulate import simulate
import copy
from generatePlayers import generate_players

# Players are represented by a number which is the value for their skill/"ELO"
# To simulate continuous time, increase amount of steps and decrease the rate players are introduced

''' TODO
- Give players some 'ID' Value
- Run matchmaking multiple times
'''
parser = argparse.ArgumentParser(description='Simulate a matchmaking scenario')

parser.add_argument('matchSize', metavar='matchSize', type=int,
    help='Number of players that make up a match for team-based simulations; must be divisible by 2')

parser.add_argument('iterations', metavar='iterations', type=int,
    help='The number of matches for which to run the simulation')

parser.add_argument('-v', action='store_true', help='Enable verbose output')

parser.add_argument('playerCount', metavar='playerCount', type=int,
    help='Number of players in the simulation; must be divisble by 2 and also match size')

parser.add_argument('skillMean', metavar='skillMean', type=float,
    help='Average true skill level of players in the simulation')

parser.add_argument('skillStdDev', metavar='skillStdDev', type=float,
					help='Standard deviation for true skill for players in the simulation')

args = parser.parse_args()

# Argument validation
if args.matchSize < 1:
    print('matchSize must be greater than 0')
    quit()
elif (args.matchSize % 2) != 0:
    print('matchSize must be divisible by 2')
    quit()

if args.iterations < 1:
    print('iterations must be greater than 1')
    quit()

if (args.playerCount % 2) != 0 or (args.playerCount % args.matchSize) != 0:
    print('playerCount must be divisible by both 2 and matchSize')
    quit()

if (args.skillMean < 0):
    print('skillMean must be non-negative')
    quit()

if (args.skillStdDev < 0):
    print('skillStdDev must be non-negative')
    quit()

''' TODO
- Give generate_players the following args: player count, skill mean, skill std dev
- Give simulate the following args: iterations (# of matches), match size 
'''

players = generate_players(args.playerCount, args.skillMean, args.skillStdDev)

# Execute the matchmaking simulation
result_1v1 = simulate(copy.deepcopy(players), args.iterations, 2)
result_mvm = simulate(copy.deepcopy(players), args.iterations, args.matchSize)

# Print results
pp = pprint.PrettyPrinter(indent=1)
print('1v1 results')
pp.pprint(result_1v1)
print('mvm results')
pp.pprint(result_mvm)
