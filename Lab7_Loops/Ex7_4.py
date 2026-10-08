recent_purchases = [36.13, 23.87, 183.35, 22.93, 11.62]
budget = 50

total_spent = 0

for purchase in recent_purchases:
    if total_spent + purchase <= budget:
        total_spent += purchase
        print(f"This purchase is within budget. Total spent: ${total_spent:.2f}")
    else:
        print(f"This purchase is over budget! Total spent: ${total_spent:.2f}")