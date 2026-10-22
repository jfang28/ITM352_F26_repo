# Step Challenge
# Three friends tracked their daily steps for one week.
# This program is supposed to:
#  1. Compute each person's average daily steps.
#  2. Award a badge based on that average:
#        Gold   - an average of 10,000 steps or more
#        Silver - an average of 7,500 steps or more
#        Bronze - anything less
#  3. Print a summary line for each person.


weekly_steps = {
   "Kai":     [8000, 9500, 7200, 11000, 6800, 12000, 9000],
   "Leilani": [12000, 9000, 10500, 8500, 11000, 9500, 9500],
   "Noa":     [4000, 5200, 3800, 6100, 4500, 5000, 4400],
}


def choose_badge(average):
   if average >= 10000:
       return "Gold"
   elif average >= 7500:
       return "Silver"
   else:
       return "Bronze"


for name, days in weekly_steps.items():
   try:
       average = sum(days) / len(days)
   except TypeError:
       print(f"Invalid step count for {name}: all daily steps must be numbers.")
       continue
   except ZeroDivisionError:
       print(f"Cannot calculate an average for {name}: no daily steps were provided.")
       continue

   badge = choose_badge(average)
   print(name.ljust(8), "average:", format(average, ",.0f"), "steps/day ->", badge)
