# Calculating a shopping cart
prices = [5.95, 3.00, 12.50]
total_price = 0
tax_rate = 0.08    # 8% tax 
for price in prices:
    total_price += price * (1+tax_rate)

print(f"Total price (with tax): ${total_price:.2f}")
