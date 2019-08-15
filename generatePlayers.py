import numpy as np


# Assume traditional ELO system with mean of 1500 (50th percentile)
# Generate a normal distribution around this mean

class Player:

    def __init__(self, id, true_skill, skill_mean):
        self.id = id
        self.true_skill = true_skill
        self.est_skill = skill_mean
    
    def __repr__(self):
        return str({ 'id': self.id, 'true_skill': self.true_skill, 'est_skill': self.est_skill })


def generate_players(count, skill_mean, skill_std_dev):

    players = []

    for x in range(count):
        skill = -1
        while skill < 0:
            skill = int(np.random.normal(loc=skill_mean, scale=skill_std_dev))

        new_player = Player(x, skill, skill_mean)
        players.append(new_player)

    return players
