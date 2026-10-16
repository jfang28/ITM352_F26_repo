def show_hint(hints, hint_index, hints_used):
    if hint_index < len(hints):
        print("Hint:", hints[hint_index])
        return hint_index + 1, hints_used + 1
    else:
        print("You have used all available hints.")
        return hint_index, hints_used