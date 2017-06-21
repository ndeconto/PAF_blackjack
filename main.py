import simulation_jeux
import algo_monte_carlo

for i in range(10000):
	simulation_jeux.manche()

def f(values):
	return values.index(max(values))

result = [[f(values) for values in i]for i in algo_monte_carlo.mypolicy]
print("      low enemy card   | high enemy card")
print("     <- low value hand  |  high value hand ->")
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in result]))
