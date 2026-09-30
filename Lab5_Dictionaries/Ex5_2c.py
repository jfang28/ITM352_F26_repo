durations = [1.1, 0.8, 2.5, 2.6]
fares = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = dict(zip(durations, fares))

print(f"3rd trip: {list(trips.items())[2][0]} miles, {list(trips.items())[2][1]}")
