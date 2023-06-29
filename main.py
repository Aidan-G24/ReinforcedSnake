
# Python Snake With reinforcement learning AI

import pygame
import numpy as np
import random



class Snake:
    def __init__(self):
        self.size = 4
        self.body = [(19, 12), (20, 12), (21, 12), (22, 12)]  # array of tuples holding every point of the snake
        self.direction = 'L'
        self.alive = True
        self.velocity = 20
        self.reward = 0

    def move_body(self):
        if self.size == len(self.body):
            self.body.pop(-1)
        if self.direction == 'L':
            self.body = [(self.body[0][0] - 1, self.body[0][1])] + self.body
        elif self.direction == 'R':
            self.body = [(self.body[0][0] + 1, self.body[0][1])] + self.body
        elif self.direction == 'U':
            self.body = [(self.body[0][0], self.body[0][1] - 1)] + self.body
        elif self.direction == 'D':
            self.body = [(self.body[0][0], self.body[0][1] + 1)] + self.body

    def change_dir(self, new_dir):
        s = {self.direction, new_dir}
        # cannot move in the exact opposite direction or same direction
        if s != {'L', 'R'} and s != {'U', 'D'} and len(s) != 1:
            self.direction = new_dir


class App:
    def __init__(self, player, agent):
        self._running = True
        self._display_surf = None
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.size = self.weight, self.height = 640, 430
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.board_size = self.board_width, self.board_height = 40, 25
        self.block_size = self.block_width, self.block_height = 16, 16
        self.board = np.chararray(self.board_size)
        self.snake = Snake()
        self.state = 0
        self.player = player
        self.agent = agent
        self.food_loc = self.place_food(self.snake.body)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Python Snake")
        self._running = True
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.snake.change_dir('R')
            elif event.key == pygame.K_LEFT:
                self.snake.change_dir('L')
            elif event.key == pygame.K_UP:
                self.snake.change_dir('U')
            elif event.key == pygame.K_DOWN:
                self.snake.change_dir('D')

    def check_alive(self, body):
        col_border, row_border = [-1, self.board_width], [-1, self.board_height]  # [col_min, col_max][row_min, row_max]
        if body[0][0] in col_border or body[0][1] in row_border:
            return False
        if len(set(body)) != len(body):
            return False
        return True

    def food_eat(self, head):
        if head == self.food_loc:
            self.snake.size += 1
            self.score += 1
            self.food_loc = self.place_food(self.snake.body)
            self.reward = 10

    def disp_object(self, body):
        self._display_surf.fill((0, 0, 0))
        self._display_surf.fill((0, 0, 255), (0, 400, 640, 30))
        for i in body:
            pygame.draw.rect(self._display_surf, (0, 255, 0),
                             (i[0] * self.block_width, i[1] * self.block_height) + self.block_size)
        pygame.draw.rect(self._display_surf, (255, 0, 0),
                         (self.food_loc[0] * self.block_width, self.food_loc[1] * self.block_height) + self.block_size)
        text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self._display_surf.blit(text, (0, 400))
        pygame.display.update()

    def place_food(self, body):
        c, r = random.randint(0, self.board_width - 1), random.randint(0, self.board_height - 1)
        while (c, r) in body:
            c, r = random.randint(0, self.board_width - 1), random.randint(0, self.board_height - 1)
        return c, r

    def get_state(self):
        # returns a number with 12 bits set as the state
        state = 0

        # determine if there is an obstacle directly next to the snake in any direction
        # obstacle to the right
        if self.snake.body[0][0] == self.board_width  or (self.snake.body[0][0] + 1, self.snake.body[0][1]) in self.snake.body[2:]:
            state |= 1 << 3
        # obstacle to the left
        if self.snake.body[0][0] == 0 or (self.snake.body[0][0] - 1, self.snake.body[0][1]) in self.snake.body[2:]:
            state |= 1 << 2
        # obstacle below
        if self.snake.body[0][1] == self.board_height or (self.snake.body[0][0], self.snake.body[0][1] + 1) in self.snake.body[2:]:
            state |= 1 << 1
        # obstacle above
        if self.snake.body[0][1] == 0 or (self.snake.body[0][0], self.snake.body[0][1] - 1) in self.snake.body[2:]:
            state |= 1

        # determine the location of the apple in reference to the snake
        # food to the right
        if self.snake.body[0][0] < self.food_loc[0]:
            state |= 1 << 7
        # food to the left
        if self.snake.body[0][0] > self.food_loc[0]:
            state |= 1 << 6
        # food below
        if self.snake.body[0][1] < self.food_loc[1]:
            state |= 1 << 5
        # food above
        if self.snake.body[0][1] > self.food_loc[1]:
            state |= 1 << 4

        # determine the direction the snake is moving
        if self.snake.direction == "R":
            state |= 1 << 11
        elif self.snake.direction == "L":
            state |= 1 << 10
        elif self.snake.direction == "D":
            state |= 1 << 9
        else:
            state |= 1 << 8

        if (state >> 7 & 1) & (state >> 11 & 1):
            self.reward = 1
        elif (state >> 6 & 1) & (state >> 10 & 1):
            self.reward = 1
        elif (state >> 5 & 1) & (state >> 9 & 1):
            self.reward = 1
        elif (state >> 4 & 1) & (state >> 8 & 1):
            self.reward = 1
        else:
            self.reward = -1
        # print(self.snake.body, bin(state))
        return state

    def on_loop(self):
        self.disp_object(self.snake.body)
        if self.player == "Human":
            self.on_event(pygame.event.poll())
        else:
            self.snake.change_dir(self.agent.make_move(self.state, self.snake.direction))
        self.snake.move_body()
        self.food_eat(self.snake.body[0])
        self.prev_state = self.state
        self.state = self.get_state()
        if not self.check_alive(self.snake.body):
            self.reward = -100
            self._running = False
        self.agent.train(self.prev_state, self.snake.direction, self.reward)
        self.clock.tick(self.snake.velocity)

    def on_execute(self):
        if not self.on_init():
            self._running = False

        while self._running:
            self.on_loop()
        pygame.quit()
        return self.score


if __name__ == "__main__":
    player = "Human"
    SnakeGame = App("Human")
    score = SnakeGame.on_execute()
    print(score)
