
import pandas as pd
import json
import urllib.request

# Load dataset once
file_path = "data/Ecommerce_Sales_Raw_Dataset - Copy.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="Cleaned E commerce sales"
)



def ask_ollama(prompt, timeout=120):
    """Use Groq in the cloud and Ollama locally."""
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

    if api_key:
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        request = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            method="POST"
        )

        with urllib.request.urlopen(
            request, timeout=timeout
        ) as response:
            data = json.loads(response.read().decode("utf-8"))

        return data["choices"][0]["message"]["content"]

    # Fall back to local Ollama
    payload = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(
        request, timeout=timeout
    ) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["response"]




def interpret_question(question):
    prompt = f"""
Convert the user's question into a JSON analysis plan.
Return ONLY a JSON object with all four keys:
dimension, metric, operation, limit.

Allowed dimensions: overall, category, region, month, product, status
Allowed metrics: sales, quantity, orders
Allowed operations: total, highest, lowest, top, compare, summary

The dimension must be the data group being analyzed,
such as category, region, month, product, or status.

The operation must describe what to do,
such as total, highest, lowest, top, compare, or summary.

Example:
Question: Compare sales across all categories.
JSON:
{{"dimension":"category","metric":"sales","operation":"compare","limit":5}}

Rules:
- best, highest, most, maximum -> highest
- lowest, worst, least, minimum -> lowest
- top N -> top, limit N (maximum 5)
- compare or breakdown -> compare
- how many orders -> overall, orders, total
- overall sales total -> overall, sales, total
- If the question mentions a category, use category.
- If it mentions a region, use region.
- If it mentions a month, use month.
- If it mentions a product, use product.
- If it mentions order status, returned, delivered, cancelled, or pending, use status.
- Otherwise, use overall.

Examples:
Question: Which is the best-performing sales category?
{{"dimension":"category","metric":"sales","operation":"highest","limit":1}}

Question: Which region has the lowest sales?
{{"dimension":"region","metric":"sales","operation":"lowest","limit":1}}

Question: Show the top 5 products by sales.
{{"dimension":"product","metric":"sales","operation":"top","limit":5}}

Question: How many orders are there?
{{"dimension":"overall","metric":"orders","operation":"total","limit":1}}

User question: {question}
"""

  plan_text = ask_ollama(prompt).strip()

if not plan_text:
    raise ValueError("AI returned an empty response.")
    try:
        plan = json.loads(plan_text)
    except json.JSONDecodeError:
        raise ValueError(
            f"Ollama returned invalid JSON: {plan_text!r}"
        )

    allowed = {
        "dimension": [
            "overall", "category", "region",
            "month", "product", "status"
        ],
        "metric": ["sales", "quantity", "orders"],
        "operation": [
            "total", "highest", "lowest",
            "top", "compare", "summary"
        ]
    }

    
    # Fix the known category comparison question
    
    # Correct dimension and operation mix-ups
    if plan.get("dimension") in allowed["operation"]:
        mistaken_operation = plan["dimension"]

        if "categor" in question.lower():
            plan["dimension"] = "category"
        elif "region" in question.lower():
            plan["dimension"] = "region"
        elif "month" in question.lower():
            plan["dimension"] = "month"
        elif "product" in question.lower():
            plan["dimension"] = "product"
        elif "status" in question.lower():
            plan["dimension"] = "status"
        else:
            plan["dimension"] = "overall"

        plan["operation"] = mistaken_operation

    # Validate the plan returned by the model

# Normalize common operation names returned by Ollama

    # Normalize common operation names returned by Ollama
    operation_aliases = {
        "best": "highest",
        "most": "highest",
        "maximum": "highest",
        "max": "highest",
        "worst": "lowest",
        "least": "lowest",
        "minimum": "lowest",
        "min": "lowest",
        "breakdown": "compare",
        "comparison": "compare",
    }

    # Fix an operation mistakenly returned as the metric
    metric_value = str(plan.get("metric", "")).strip().lower()

    if metric_value in operation_aliases:
        plan["metric"] = "sales"
        plan["operation"] = operation_aliases[metric_value]

    # Normalize the operation field
    operation = str(plan.get("operation", "")).strip().lower()
    plan["operation"] = operation_aliases.get(operation, operation)

    # Validate the plan returned by the model
    for field, choices in allowed.items():
        if plan.get(field) not in choices:
            raise ValueError(
                f"Invalid analysis plan: {field}. "
                f"Received: {plan.get(field)!r}"
            )

   

    try:
        limit = int(plan.get("limit", 1))
    except (ValueError, TypeError):
        limit = 1

    plan["limit"] = max(1, min(limit, 5))

    return plan


def execute_analysis(plan):
    dimension = plan.get("dimension")
    metric = plan.get("metric")
    operation = plan.get("operation")
    limit = plan.get("limit", 1)

    if dimension == "overall":
        if metric == "orders":
            value = df["Order ID"].nunique()
            return f"Total orders: {value}"
        elif metric == "sales":
            return f"Total sales: ₹{df['Sales Amount'].sum():,.2f}"
        elif metric == "quantity":
            return f"Total quantity: {df['Quantity'].sum()}"
        return "This metric is not supported."

    group_columns = {
        "category": "Category",
        "region": "Region",
        "month": "Month Name",
        "product": "Product",
        "status": "Order Status"
    }

    column_map = {
        "sales": "Sales Amount",
        "quantity": "Quantity",
        "orders": "Order ID"
    }

    group_column = group_columns.get(dimension)
    column = column_map.get(metric)

    if group_column is None or column is None:
        return "This question is not supported yet."

    if metric == "orders":
        result = df.groupby(group_column)[column].nunique()
    else:
        result = df.groupby(group_column)[column].sum()

    if dimension == "region":
        result = result.drop(labels=["Not given"], errors="ignore")

    if result.empty:
        return "No results found."

    if operation == "highest":
        return f"Highest: {result.idxmax()} — {result.max():,.2f}"

    if operation == "lowest":
        return f"Lowest: {result.idxmin()} — {result.min():,.2f}"

    if operation == "top":
        return result.sort_values(ascending=False).head(limit).to_string()

    if operation in ["compare", "summary"]:
        return result.sort_values(ascending=False).to_string()

    if operation == "total":
        return f"Total: {result.sum():,.2f}"

    return "Unsupported analysis operation."




def generate_explanation(question, result):
    prompt = f"""
You are a careful business data analyst for an e-commerce company.

USER QUESTION:
{question}

ACTUAL ANALYSIS RESULT:
{result}

RULES:
1. Explain only what the actual analysis result supports.
2. Never introduce new numbers, metrics, products, categories, or regions.
3. Never claim a value is highest or lowest unless the result explicitly supports it.
4. If the result contains total orders, report the order count only.
5. If the result contains a comparison, describe it using only the values provided.
6. Give a practical business interpretation only when justified by the result.
7. If the result lacks enough information, clearly say so.
8. Use ₹ and Indian number formatting for currency values already provided.
9. Return exactly 2 simple sentences.
10. Do not use Markdown or invent additional figures.
11. Before responding, verify that every number and ranking matches
    the actual analysis result.
12. Never confuse sales amount with order quantity or order count.

Write the explanation now:
"""
    return ask_ollama(prompt)
