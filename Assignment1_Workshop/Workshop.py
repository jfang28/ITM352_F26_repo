import random

questions = {
     "What is the airspeed of an unladen swallow in miles/hr": {
          "options": {"a": "12", "b": "8", "c": "11", "d": "15"},
          "correct": "c"
     },
     "What is the capital of Texas": {
          "options": {"a": "Austin", "b": "San Antonio", "c": "Dallas", "d": "Waco"},
          "correct": "a"
     },
     "The Last Supper was painted by which artist": {
          "options": {"a": "Da Vinci", "b": "Rembrandt", "c": "Picasso", "d": "Michelangelo"},
          "correct": "a"
     },
     "Which classic novel opens with the line 'Call Me Ishmael'?": {
          "options": {"a": "Moby Dick", "b": "Wuthering Heights", "c": "The Old Man and the Sea", "d": "The Scarlet Letter"},
          "correct": "a"
     },
     "Frank Lloyd Wright designed a house that included a waterfall. What is the name of this house?": {
          "options": {"a": "Fallingwater", "b": "Watering Heights", "c": "Mossyledge", "d": "Taliesin"},
          "correct": "a"
     }
}

score = 0
question_order = list(questions.items())
random.shuffle(question_order)

for question, details in question_order:
     correct_option = details["options"][details["correct"]]
     shuffled_options = list(details["options"].values())
     random.shuffle(shuffled_options)
     option_labels = ["a", "b", "c", "d"]
     details["options"] = dict(zip(option_labels, shuffled_options))

     for label, option in details["options"].items():
          if option == correct_option:
               details["correct"] = label

     print(question)
     for label, option in details["options"].items():
          print(f"{label}. {option}")
     user_answer = input("Your answer (a, b, c, or d): ").strip().lower()

     if user_answer == details["correct"]:
          print("Correct!")
          score += 1
     else:
          correct_label = details["correct"]
          correct_option = details["options"][correct_label]
          print(f"Incorrect. The correct answer is {correct_label}. {correct_option}.")

print(f"You got {score} out of {len(questions)} correct.")