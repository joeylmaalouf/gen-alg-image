from PIL import Image, ImageDraw
import os
from random import randint
import sys


class Ellipse (object):
  def __init__ (self, resolution):
    self.resolution = resolution
    for i in range(5):
      self.randomize(i)

  def randomize (self, attribute_index):
    if attribute_index == 0:
      self.xcoord = randint(0, self.resolution[0] - 1)
    elif attribute_index == 1:
      self.ycoord = randint(0, self.resolution[1] - 1)
    elif attribute_index == 2:
      self.xradius = randint(1, self.resolution[0] - 1)
    elif attribute_index == 3:
      self.yradius = randint(1, self.resolution[1] - 1)
    elif attribute_index == 4:
      self.brightness = randint(0, 255)


class Individual (object):
  def __init__ (self, resolution):
    self.n_ellipses = 20
    self.solution = [Ellipse(resolution) for _ in range(self.n_ellipses)]
    self.fitness = 0

  def make_image (self, resolution):
    self.image = Image.new("L", resolution)
    draw = ImageDraw.Draw(self.image)
    for i in range(self.n_ellipses):
      ellipse = self.solution[i]
      bounds = (ellipse.xcoord - ellipse.xradius, ellipse.ycoord - ellipse.yradius,
                ellipse.xcoord + ellipse.xradius, ellipse.ycoord + ellipse.yradius)
      draw.ellipse(bounds, fill = ellipse.brightness)

  def mutate (self):
    i = randint(0, self.n_ellipses - 1)
    j = randint(0, 4)
    self.solution[i].randomize(j)

  def scramble (self, n = 100):
    for _ in range(n):
      self.mutate()

  def payoff (self, resolution, goal_access):
    diff = 0
    self_access = self.image.load()
    for i in range(resolution[0]):
      for j in range(resolution[1]):
        diff += abs(self_access[i, j] - goal_access[i, j])
    self.fitness = diff ** 2


def main (goal_path, popsize, generations, step):
  folder_path = goal_path + " images"
  if not os.path.isdir(folder_path):
    os.mkdir(folder_path)
  goal_image = Image.open(goal_path).convert("L")
  goal_access = goal_image.load()
  resolution = goal_image.size
  population = [Individual(resolution) for i in range(popsize)]
  generation = 0
  while(generation < generations):
    for individual in population:
      individual.make_image(resolution)
      individual.payoff(resolution, goal_access)
    population.sort(key = lambda x: x.fitness)
    if generation % 100 == 0:
      population[0].image.save(
        "{0}/gen {1}, off by {2}.jpg".format(
          folder_path, generation, population[0].fitness
        )
      )
    for individual in population[popsize // 4:popsize // 2]:
      individual.mutate()
    for individual in population[popsize // 2:]:
      individual.scramble()
    generation += 1
    print(generation)


if __name__ == "__main__":
  goal_path = "goal.jpg" if len(sys.argv) < 2 else sys.argv[1]
  popsize = 1000 if len(sys.argv) < 3 else int(sys.argv[2])
  generations = 2000 if len(sys.argv) < 4 else int(sys.argv[3])
  step = 100 if len(sys.argv) < 5 else int(sys.argv[4])
  main(goal_path, popsize, generations, step)
