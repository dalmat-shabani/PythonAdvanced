import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from expense_app.authentication.database import get_expenses


def plot_monthly_expenses(user_id):
    expenses = get_expenses(user_id)
    print("EXPENSES:", expenses)

    monthly_totals = defaultdict(float)

    for exp in expenses:
        # exp structure: (date, category, amount, description)
        exp_date = exp[0]  # 'YYYY-MM-DD'
        amount = float(exp[2])  # amount

        month = exp_date[:7]  # 'YYYY-MM'
        monthly_totals[month] += amount

    if not monthly_totals:
        print("NO DATA TO PLOT")
        return

    # Get the range of months (from first to last month)
    months = sorted(monthly_totals.keys())
    first_month = months[0]
    last_month = months[-1]

    # Generate all months between first and last month
    all_months = []
    current = first_month
    year, month = map(int, current.split('-'))

    while True:
        all_months.append(f"{year}-{month:02d}")
        # Increment month
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        current = f"{year}-{month:02d}"
        if current > last_month:
            break

    # Ensure each month in all_months has a total, even if zero
    totals = [monthly_totals.get(m, 0) for m in all_months]

    print("ALL MONTHS:", all_months)
    print("TOTALS:", totals)

    # Plotting
    x = np.arange(len(all_months))
    plt.figure(figsize=(13, 10))
    plt.bar(x, totals, width=0.2)

    plt.xticks(x, all_months)
    plt.title("Monthly Expenses")
    plt.xlabel("Month")
    plt.ylabel("Total Spent")
    plt.tight_layout()
    plt.show()