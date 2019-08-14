import argparse
import numpy as np

# Assume traditional ELO system with mean of 1500 (50th percentile)
# Generate a normal distribution around this mean

parser = argparse.ArgumentParser(description='Generate a normal distribution of players (ELOs) to use in a simulation.')

parser.add_argument('listSize', metavar='n', type=int, help='The size of the generated list')

args = parser.parse_args()

# Argument Validation
if (args.listSize <= 0):
	print('Size must be positive')
	quit()

mean = 1500

randomNums = np.random.normal(loc=mean, scale=(mean/3), size=args.listSize)
randomInts = list(map(int, (np.round(randomNums))))

# Print the result to be redirected to a players list file
print(*randomInts)
