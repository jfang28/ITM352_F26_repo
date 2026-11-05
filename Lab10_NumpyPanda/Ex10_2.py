#List of individuals' ages
import pandas as pd


ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]
#List of individuals' names
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
#List of individuals' genders
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]

age_gender = list(zip(ages, gender))

print(age_gender)

#dataframe
dataframe = pd.DataFrame(age_gender, index=names, columns=["Age", "Gender"])

print("\nDataFrame:")
print(dataframe)

print("\nDataFrame summary:")
print(dataframe.describe())

print("\nAverage age by gender:")
print(dataframe.groupby("Gender")["Age"].mean())
