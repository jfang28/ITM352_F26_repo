import json
import sys
from pathlib import Path

# Make Assignment 1's questions module available to this program.
assignment_path = Path(__file__).parent.parent / "Assignment1"
sys.path.insert(0, str(assignment_path))

from questions import questions

json_path = Path(__file__).with_name("quiz_questions.json")

with json_path.open("w", encoding="utf-8") as json_file:
    json.dump(questions, json_file, indent=4)

print(f"Saved {len(questions)} questions to {json_path.name}.")