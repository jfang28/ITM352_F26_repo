#welcome the user
import time
print("Welcome to the quiz!")
time.sleep(1)
print("You will be asked a series of questions. Please select the correct answer from the options provided.")
time.sleep(4)
print("Each correct answer will earn you 1 point. Each incorrect answer will deduct 1 point.")
time.sleep(4)
print("Each question has 1 hint available. You can get a hint by typing 'hint'.")
time.sleep(3)
print("Would you like to begin?")
time.sleep(1)
user_start = input("Type 'yes' to begin: ").strip().lower()
time.sleep(1)
if user_start != "yes":
    print(":( Please reconsider.")
    exit()

#quiz questions/hints
from questions import questions
from quiz_functions import show_hint

#ask user question, display options, ask if hint needed, display correct answer
points = 0
for question in questions:
    print(question["question"])
    for option in question["options"]:
        print(option)
    user_answer = input("Your answer (select letter): ").strip().upper()
    while True:
        if user_answer.lower() == "hint":
            show_hint(question["hint"])
            user_answer = input("Your answer (select letter): ").strip().upper()
            continue
        if user_answer not in ["A", "B", "C", "D"]:
            print("Invalid answer. Please select a letter (A, B, C, D).")
            user_answer = input("Your answer (select letter): ").strip().upper()
            continue
        if user_answer == question["answer"]:
            print("Correct!")
            points += 1
        else:
            if points > 0:
                points -= 1
            print("Sorry :(. The correct answer is", question["answer"])
        break

#display final score
print("Your final score is", points)