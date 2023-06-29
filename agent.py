
import random
from main import App
from matplotlib import pyplot


class Agent:
    def __init__(self, exp):
        self.states = {}    # key: tuple of state and action, value: reward
        self.explore = exp

    def train(self, prev_state, action, reward):
        key = (prev_state, action)
        if key in self.states:
            self.states[key] += reward
        else:
            self.states[key] = reward

    def make_move(self, state, direction):

        # create a list of the possible moves
        if direction == 'R' or direction == 'L':
            possible_moves = [direction, 'U', 'D']
        else:
            possible_moves = [direction, 'L', 'R']

        # determine which move has the highest value
        best = -1000000
        move = direction
        for m in possible_moves:
            key = (state, m)
            if key not in self.states:
                self.states[key] = 0
            if self.states[key] > best:
                best = self.states[key]
                move = m

        if random.uniform(0, 1) < self.explore:
            # take random action
            return possible_moves[random.randint(0, 2)]
        else:
            return move


if __name__ == "__main__":
    repeat = 1000
    group_score = 25
    expl_rate = 0
    ai = Agent(expl_rate)
    score = 0
    res = []
    for i in range(repeat):
        if i % group_score == 0:
            print(i, score)
            res.append(score/group_score)
            score = 0
        snakeGame = App("ai_player", ai)
        score += snakeGame.on_execute()

    res.append(score/group_score)
    x = [i * group_score for i in range(1, len(res) + 1)]
    pyplot.plot(x, res)
    pyplot.xlabel(f"Number of Games Played")
    pyplot.ylabel("Average Score per Game")
    pyplot.title("Results of Reinforcement Learning Snake")
    pyplot.show()

    f = open('Data.txt', 'w')
    for i in res:
        f.write(str(i)+"\n")

    f.close()
