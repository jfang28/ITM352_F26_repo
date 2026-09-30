durations = [1.1, 0.8, 2.5, 2.6]
costs = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = [
	{"miles": durations[0], "fares": costs[0]},
	{"miles": durations[1], "fares": costs[1]},
	{"miles": durations[2], "fares": costs[2]},
	{"miles": durations[3], "fares": costs[3]}
]

print(f"3rd trip: {trips[2]['miles']} miles, {trips[2]['fares']}")
