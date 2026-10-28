import pandas as pd
file_path = "data/Ecommerce_Sales_Raw_Dataset - Copy.xlsx"
df = pd.read_excel(
    file_path,
    sheet_name="Cleaned E commerce sales"
)
print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nColumns:")
print(df.columns.tolist())
print("\nFirst 5 records:")
print(df.head())
print("\n--- SALES INSIGHTS ---")
total_sales = df["Sales Amount"].sum()
print("Total Sales:", total_sales)
total_quantity = df["Quantity"].sum()
print("Total Quantity Sold:", total_quantity)
category_sales = df.groupby("Category")["Sales Amount"].sum()
best_category = category_sales.idxmax()
print("Best Category:", best_category)
region_sales = df.groupby("Region")["Sales Amount"].sum()
best_region = region_sales.idxmax()
print("Best Region:", best_region)
product_sales = df.groupby("Product")["Sales Amount"].sum()
top_products = product_sales.sort_values(ascending=False).head(5)
print("\nTop 5 Products:")
print(top_products)
print("\n--- AI GENERATED INSIGHTS ---")

# Category insight
best_category_sales = category_sales.max()

print(
    f"Electronics is the highest-performing category, "
    f"generating ₹{best_category_sales:,.2f} in sales."
)

# Region insight
best_region_sales = region_sales.max()

print(
    f"The {best_region} region generated the highest sales "
    f"with ₹{best_region_sales:,.2f}."
)

# Product insight
best_product = product_sales.idxmax()
best_product_sales = product_sales.max()

print(
    f"{best_product} is the top-selling product, "
    f"generating ₹{best_product_sales:,.2f} in sales."
)
print("\n--- MONTHLY SALES ANALYSIS ---")

monthly_sales = df.groupby("Month Name")["Sales Amount"].sum()

# Sort by month number
monthly_sales = monthly_sales.sort_values(ascending=False)

best_month = monthly_sales.index[0]
best_month_sales = monthly_sales.iloc[0]

worst_month = monthly_sales.index[-1]
worst_month_sales = monthly_sales.iloc[-1]

print(f"Best Sales Month: {best_month}")
print(f"Sales: ₹{best_month_sales:,.2f}")

print(f"\nLowest Sales Month: {worst_month}")
print(f"Sales: ₹{worst_month_sales:,.2f}")

print("\nMonthly Sales:")
print(monthly_sales)
print("\n--- BUSINESS RECOMMENDATIONS ---")

# Category recommendation
print(
    f"Recommendation: Focus more on the {best_category} category "
    f"because it has the highest sales."
)

# Region recommendation
print(
    f"Recommendation: Analyze successful strategies in the {best_region} "
    f"region and consider applying them to lower-performing regions."
)

# Monthly recommendation
print(
    f"Recommendation: Investigate why sales were lowest in {worst_month} "
    f"and identify ways to improve performance during that period."
)
print("\n--- ASK YOUR DATA ---")

def answer_question(question):

    question = question.lower()

    if "highest" in question and "category" in question:
        print(f"Answer: {best_category} has the highest sales.")

    elif "highest" in question and "region" in question:
        print(f"Answer: {best_region} has the highest sales.")

    elif "top" in question and "product" in question:
        print("Answer: The top 5 products are:")
        print(top_products)

    elif "best" in question and "month" in question:
        print(f"Answer: {best_month} had the highest sales.")

    elif "lowest" in question and "month" in question:
        print(f"Answer: {worst_month} had the lowest sales.")

    elif "total sales" in question:
        print(f"Answer: Total sales are ₹{total_sales:,.2f}.")

    else:
        print("Sorry, I don't understand that question yet.")


question = input("\nAsk a question about your sales data: ")

answer_question(question)