import simulation_jeux
import algo_monte_carlo

training_time = 1000000
testing_time = 10000

for i in range(training_time):
	simulation_jeux.manche(True)

score = 0
for i in range(testing_time):
	score += simulation_jeux.manche(False)

def f(values):
	return values.index(max(values))
	
for m in algo_monte_carlo.mypolicy:
	result = [[f(values) for values in i]for i in m]
	print("     ↑ low enemy card   | high enemy card ↓")
	print("     <- low value hand  |  high value hand ->")
	print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in result]))

print("\nAverage score : " + str(int(score*50/testing_time)) + "%")
