import json
from pathlib import Path

json_path = Path(__file__).with_name("quiz_questions.json")

with json_path.open("r", encoding="utf-8") as json_file:
    questions = json.load(json_file)

print(json.dumps(questions, indent=4))