from PIL import Image, ImageDraw
from random import randint
from sys import argv


class Ellipse(object):
	def __init__(self, resolution):
		self.resolution = resolution
		for i in range(5):
			self.randomize(i)

	def randomize(self, attribute_index):
		if attribute_index == 0:
			self.xcoord = randint(0, self.resolution[0]-1)
		elif attribute_index == 1:
			self.ycoord = randint(0, self.resolution[1]-1)
		elif attribute_index == 2:
			self.xradius = randint(1, (self.resolution[0]-1)/2)
		elif attribute_index == 3:
			self.yradius = randint(1, (self.resolution[1]-1)/2)
		elif attribute_index == 4:
			self.brightness = randint(0, 255)


class Individual(object):
	def __init__(self, resolution):
		self.n_ellipses = 20
		self.solution = []
		for i in range(self.n_ellipses):
			self.solution.append(Ellipse(resolution))
		self.fitness = 0

	def make_image(self, resolution):
		self.image = Image.new("L", resolution)
		draw = ImageDraw.Draw(self.image)
		for i in range(self.n_ellipses):
			ellipse = self.solution[i]
			bounds = (ellipse.xcoord-ellipse.xradius, ellipse.ycoord-ellipse.yradius,
					  ellipse.xcoord+ellipse.xradius, ellipse.ycoord+ellipse.yradius)
			draw.ellipse(bounds, fill = ellipse.brightness)

	def mutate(self):
		i = randint(0, self.n_ellipses-1)
		self.solution[i].randomize(randint(0, 4))

	def scramble(self):
		for i in range(self.n_ellipses*5):
			self.mutate()

	def payoff(self, resolution, goal_access):
		diff = 0
		self_access = self.image.load()
		for i in range(resolution[0]):
			for j in range(resolution[1]):
				diff += abs(self_access[i, j]-goal_access[i, j])
		self.fitness = diff**2


def main(argv):
	goal_image = Image.open("goal.jpg").convert("L")
	goal_access = goal_image.load()
	resolution = goal_image.size
	popsize = 500
	population = [Individual(resolution) for i in range(popsize)]
	generation = 0
	while(generation < 1000):
		for individual in population:
			individual.make_image(resolution)
			individual.payoff(resolution, goal_access)
		population.sort(key = lambda x: x.fitness)
		population[0].image.save("generations/"+str(generation)+"-"+str(population[0].fitness)+".jpg")
		for individual in population[popsize//4:popsize//2]:
			individual.mutate()
		for individual in population[popsize//2:]:
			individual.scramble()
		generation += 1


if __name__ == "__main__":
	main(argv)
