recent_purchases = [36.13, 23.87, 183.35, 22.93, 11.62]
budget = 50

def check_purchases(purchases, budget):
    total_spent = 0
    accepted_purchases = []
    messages = []

    for purchase in purchases:
        if total_spent + purchase <= budget:
            total_spent += purchase
            accepted_purchases.append(purchase)
            messages.append("This purchase is within budget")
        else:
            messages.append("This purchase is over budget!")

    return accepted_purchases, total_spent, messages

# Test: reject purchases that exceed the remaining budget.
accepted, total, messages = check_purchases([36, 23, 10], 50)
assert accepted == [36, 10]
assert total == 46
assert messages == [
    "This purchase is within budget",
    "This purchase is over budget!",
    "This purchase is within budget",
]

# Process the recent purchases
accepted, total, messages = check_purchases(recent_purchases, budget)

for message in messages:
    print(message)

print(f"Accepted purchases: {accepted}")
print(f"Total spent: ${total:.2f}")