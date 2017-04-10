from PIL import Image, ImageDraw
import os
from random import choice, randint
import sys
from time import time


class Triangle (object):
  def __init__ (self, resolution, attributes = {}):
    self.resolution = resolution
    self.attributes = {
      "x1": 0, "y1": 0,
      "x2": 0, "y2": 0,
      "x3": 0, "y3": 0,
      "r":  0, "g":  0, "b":  0, "a":  0
    }
    for attrib in self.attributes.keys():
      if attrib in attributes.keys():
        self.attributes[attrib] = attributes[attrib]
      else:
        self.randomize(attrib)

  def randomize (self, attribute):
    if   attribute == "x1":
      self.attributes["x1"] = randint(0, self.resolution[0] - 1)
    elif attribute == "y1":
      self.attributes["y1"] = randint(0, self.resolution[1] - 1)
    elif attribute == "x2":
      self.attributes["x2"] = randint(0, self.resolution[0] - 1)
    elif attribute == "y2":
      self.attributes["y2"] = randint(0, self.resolution[1] - 1)
    elif attribute == "x3":
      self.attributes["x3"] = randint(0, self.resolution[0] - 1)
    elif attribute == "y3":
      self.attributes["y3"] = randint(0, self.resolution[1] - 1)
    elif attribute == "r":
      self.attributes["r"] = randint(0, 255)
    elif attribute == "g":
      self.attributes["g"] = randint(0, 255)
    elif attribute == "b":
      self.attributes["b"] = randint(0, 255)
    elif attribute == "a":
      self.attributes["a"] = randint(0, 255)


class Individual (object):
  def __init__ (self, resolution, numchrom):
    self.resolution = resolution
    self.numchrom = numchrom
    self.solution = [Triangle(self.resolution) for _ in range(numchrom)]
    self.fitness = 0

  def make_image (self):
    self.image = Image.new("RGB", self.resolution)
    draw = ImageDraw.Draw(self.image)
    for triangle in self.solution:
        draw.polygon([(triangle.attributes["x1"], triangle.attributes["y1"]),
                      (triangle.attributes["x2"], triangle.attributes["y2"]),
                      (triangle.attributes["x3"], triangle.attributes["y3"])],
                     fill = (triangle.attributes["r"],
                             triangle.attributes["g"],
                             triangle.attributes["b"],
                             triangle.attributes["a"]))

  def evolve (self):
    target = choice(self.solution)
    target.randomize(choice(target.attributes.keys()))

  def payoff (self, goal_access):
    self_access = self.image.load()
    diff = 0
    for i in range(self.resolution[0]):
      for j in range(self.resolution[1]):
        self_pix = self_access[i, j]
        goal_pix = goal_access[i, j]
        diff += abs(self_pix[0] - goal_pix[0])
        diff += abs(self_pix[1] - goal_pix[1])
        diff += abs(self_pix[2] - goal_pix[2])
    self.fitness = diff ** 2

  def copy (self):
    copy = Individual(self.resolution, self.numchrom)
    copy.solution = [Triangle(self.resolution, triangle.attributes) for triangle in self.solution]
    return copy


def main (goal_path, popsize, numchrom, generations, step):
  folder_path = goal_path + " images"
  if not os.path.isdir(folder_path):
    os.mkdir(folder_path)
  goal_image = Image.open(goal_path).convert("RGB")
  goal_access = goal_image.load()
  resolution = goal_image.size
  population = [Individual(resolution, numchrom) for i in range(popsize)]
  generation = 0
  while(generation < generations):
    for individual in population:
      individual.make_image()
      individual.payoff(goal_access)
    population.sort(key = lambda x: x.fitness)
    if generation % step == 0:
      population[0].image.save(
        "{0}/{1}-{2}-{3}.jpg".format(
          folder_path, int(time()), generation, population[0].fitness
        )
      )
    for i in range(len(population)):
      if i > 0:
        population[i] = population[0].copy()
      population[i].evolve()
    generation += 1


if __name__ == "__main__":
  goal_path   = "goal.jpg" if len(sys.argv) < 2 else sys.argv[1]
  popsize     = 1000       if len(sys.argv) < 3 else int(sys.argv[2])
  numchrom    = 100        if len(sys.argv) < 4 else int(sys.argv[3])
  generations = 2001       if len(sys.argv) < 5 else int(sys.argv[4])
  step        = 100        if len(sys.argv) < 6 else int(sys.argv[5])
  main(goal_path, popsize, numchrom, generations, step)
