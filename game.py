from tensorflow.keras.models import load_model
import random
import numpy as np
import pygame
import time

FPS = 30

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
# pygame.mixer.init()  # For sound
pygame.font.init()
pygame.display.set_caption("2048")


class Game:
    def __init__(self, player="human", width=4, height=4):
        self.width = width
        self.height = height
        self.blocksize = 100

        # initialize pygame and create window
        self.screen = pygame.display.set_mode(
            (self.width * self.blocksize, self.height * self.blocksize + 70))
        self.clock = pygame.time.Clock()  # For syncing the FPS

        self.my_font = pygame.font.SysFont('Comic Sans MS', 60)
        self.my_font1 = pygame.font.SysFont('Comic Sans MS', 30)

        self.score = 0
        self.player = player

    def step(self, action):
        change = False
        if action == 0:  # LEFT
            # Combining the blocks
            for i in range(self.height):
                for j in range(self.width):
                    if self.map[i, j] != 0:
                        for k in range(j+1, self.width):
                            if self.map[i, k] != 0 and self.map[i, k] == self.map[i, j]:
                                self.map[i, j] *= 2
                                self.map[i, k] = 0
                                self.score += self.map[i, j]
                                change = True
                                break

            # Moving the blocks
            for i in range(self.height):
                for j in range(self.width):
                    if self.map[i, j] == 0:
                        for k in range(j+1, self.width):
                            if self.map[i, k] != 0:
                                self.map[i, j:-(self.width -
                                                len(self.map[i, k:]) - j)] = self.map[i, k:]
                                self.map[i, -(self.width -
                                              len(self.map[i, k:]) - j):] = 0
                                change = True
                                break
        elif action == 1:  # RIGHT
            # Combining the blocks
            for i in range(self.height):
                for j in range(self.width-1, -1, -1):
                    if self.map[i, j] != 0:
                        for k in range(j-1, -1, -1):
                            if self.map[i, k] != 0 and self.map[i, k] == self.map[i, j]:
                                self.map[i, j] *= 2
                                self.map[i, k] = 0
                                self.score += self.map[i, j]
                                change = True
                                break

            # Moving the blocks
            for i in range(self.height):
                for j in range(self.width-1, -1, -1):
                    if self.map[i, j] == 0:
                        for k in range(j-1, -1, -1):
                            if self.map[i, k] != 0:
                                self.map[i, -(len(self.map[i, :k+1]) +
                                              (3 - j)): j + 1] = self.map[i, :k+1]

                                self.map[i, : -
                                         (len(self.map[i, :k+1]) + (3 - j))] = 0

                                change = True
                                break
            pass
        elif action == 2:  # UP
            # Combining the blocks
            for j in range(self.width):
                for i in range(self.height):
                    if self.map[i, j] != 0:
                        for k in range(i+1, self.height):
                            if self.map[k, j] != 0 and self.map[k, j] == self.map[i, j]:
                                self.map[i, j] *= 2
                                self.map[k, j] = 0
                                self.score += self.map[i, j]
                                change = True
                                break

            # Moving the blocks
            for j in range(self.width):
                for i in range(self.height):
                    if self.map[i, j] == 0:
                        for k in range(i+1, self.height):
                            if self.map[k, j] != 0:
                                self.map[i:-(self.height -
                                             len(self.map[k:, j]) - i), j] = self.map[k:, j]
                                self.map[-(self.height -
                                           len(self.map[k:, j]) - i):, j] = 0
                                change = True
                                break
        elif action == 3:  # DOWN
            # Combining the blocks
            for j in range(self.width):
                for i in range(self.height-1, -1, -1):
                    if self.map[i, j] != 0:
                        for k in range(i-1, -1, -1):
                            if self.map[k, j] != 0 and self.map[k, j] == self.map[i, j]:
                                self.map[i, j] *= 2
                                self.map[k, j] = 0
                                self.score += self.map[i, j]
                                change = True
                                break

            # Moving the blocks
            for j in range(self.width):
                for i in range(self.height-1, -1, -1):
                    if self.map[i, j] == 0:
                        for k in range(i-1, -1, -1):
                            if self.map[k, j] != 0:
                                self.map[-(len(self.map[:k+1, j]) +
                                           (3 - i)): i + 1, j] = self.map[:k+1, j]

                                self.map[: -
                                         (len(self.map[:k+1, j]) + (3 - i)), j] = 0

                                change = True
                                break

        else:
            raise ValueError("Invalid action")

        if change:
            self.addRandomBlock()

        self.render()  # Uncomment this to see the game in action

        return self.map

    def render(self):
        # will make the loop run at the same speed all the time
        self.clock.tick(FPS)
        self.screen.fill(BLACK)

        for i in range(self.blocksize, self.width * self.blocksize + 1, self.blocksize):
            pygame.draw.line(self.screen, RED, (i, 0),
                             (i, self.height * self.blocksize))

        for i in range(self.blocksize, self.height * self.blocksize + 1, self.blocksize):
            pygame.draw.line(self.screen, RED, (0, i),
                             (self.width * self.blocksize, i))

        for i in range(self.height):
            for j in range(self.width):
                val = self.map[i, j]
                if int(val) != 0:
                    self.drawBlock(i, j, val)

        text_surface = self.my_font1.render(
            str(f'{self.username}      Score: {int(self.getScore())}'), False, WHITE)
        self.screen.blit(
            text_surface, (self.width / 2 * self.blocksize - text_surface.get_width() / 2, self.height * self.blocksize + text_surface.get_height() / 2))

        if self.player == "human":
            text_surface2 = self.my_font1.render(
                str(f'HighScore: {max(self.scoreList)} By: {self.highScoreBy}'), False, WHITE)
            self.screen.blit(
                text_surface2, (self.width / 2 * self.blocksize - text_surface2.get_width() / 2, self.height * self.blocksize + text_surface2.get_height() / 2 + 35))

        pygame.display.flip()

    def drawBlock(self, i, j, val):
        x = j * self.blocksize
        y = i * self.blocksize

        pygame.draw.rect(
            self.screen, self.blockColor[int(val)], (x, y, self.blocksize, self.blocksize))

        text_surface = self.my_font.render(str(int(val)), False, WHITE)
        self.screen.blit(
            text_surface, (x + self.blocksize / 2 - text_surface.get_width() / 2, y + self.blocksize / 2 - text_surface.get_height() / 2))

    def getScore(self):
        return self.score

    def addRandomBlock(self):
        freeSpace = []
        for i in range(self.height):
            for j in range(self.width):
                if int(self.map[i, j]) == 0:
                    freeSpace.append((i, j))

        pos = random.choice(freeSpace)
        self.map[pos] = 2 if random.random() < 0.9 else 4

    def reset(self):
        self.map = np.zeros((self.height, self.width))
        self.map[random.randint(0, self.height-1),
                 random.randint(0, self.width-1)] = 2

        self.username = ("Human-" if self.player.lower() ==
                         "human" else "AI-") + str(int(time.time()))
        self.score = 0

        # Map 2, 4, 8 with random color
        self.blockColor = {}
        for i in range(1, 50):
            self.blockColor[2 ** i] = [random.randint(
                0, 240), random.randint(0, 240), random.randint(0, 240)]

        # Read ScoreList
        self.scoreList = []
        self.highScoreBy = ""

        if self.player == "human":
            try:
                file = open("2048ScoreList.txt", "r")
            except:
                file = open("2048ScoreList.txt", "w+")
                file.write("None : 0")
                file.close()

            file = open("2048ScoreList.txt", "r")

            for line in file.readlines():
                lineData = line.split(" : ")
                self.scoreList.append(int(lineData[1]))
                self.highScoreBy = lineData[0]

        return self.map

    def isDone(self):
        isZero = False
        sameAdj = False
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i, j] == 0:
                    isZero = True
                if i < self.height - 1 and self.map[i, j] == self.map[i+1, j]:
                    sameAdj = True
                if j < self.width - 1 and self.map[i, j] == self.map[i, j+1]:
                    sameAdj = True

        return not isZero and not sameAdj


# Run the game
# env = Game()

# env.reset()
# running = True
# frame = 1

# while running:
#     for event in pygame.event.get():
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT]:
#             env.step(0)
#         if keys[pygame.K_RIGHT]:
#             env.step(1)
#         if keys[pygame.K_UP]:
#             env.step(2)
#         if keys[pygame.K_DOWN]:
#             env.step(3)

#         if event.type == pygame.QUIT:
#             running = False
#             pygame.quit()
#             break

#     running = running and (not env.isDone())
#     frame += 1

# file = open("2048ScoreList.txt", "a")
# file.write(f"\n{env.username} : {int(env.score)}")
# file.close()


# Playing model --------------------


env = Game()
env.reset()

model = load_model("model-epoch59-score-1860.h5")


old_state = env.reset().reshape(1, 16)
done = False
frame = 0
FRAMES = 150
while not done:
    frame += 1
    action = np.argmax(model.predict(old_state))
    print(action)
    next_state = env.step(action).reshape(16)
    reward = env.score
    done = done or env.isDone() or frame > FRAMES
    state = next_state
    print("Frame", frame)

    if done:
        break
