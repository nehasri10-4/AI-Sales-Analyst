
import streamlit as st
from ai_engine import (
    df,
    interpret_question,
    execute_analysis,
    generate_explanation
)

st.set_page_config(
    page_title="AI Analysis & Insights",
    page_icon="🤖",
    layout="wide"
)

st.title("💡 Automatic Business Insights")
st.caption("Key findings from your currently loaded sales data.")

# ---------- CALCULATE INSIGHTS ----------
total_sales = df["Sales Amount"].sum()

category_sales = df.groupby("Category")["Sales Amount"].sum()

region_data = df[df["Region"] != "Not given"]
region_sales = region_data.groupby("Region")["Sales Amount"].sum()

product_sales = df.groupby("Product")["Sales Amount"].sum()

monthly_sales = df.groupby("Month Name")["Sales Amount"].sum()

# ---------- AUTOMATIC BUSINESS INSIGHTS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("🏆 **Top Category**")
    st.success(
        f"{category_sales.idxmax()}\n\n"
        f"Sales: ₹{category_sales.max():,.2f}"
    )

with col2:
    st.markdown("🌍 **Top Region**")
    st.success(
        f"{region_sales.idxmax()}\n\n"
        f"Sales: ₹{region_sales.max():,.2f}"
    )

with col3:
    st.markdown("🗓️ **Best Sales Month**")
    st.success(
        f"{monthly_sales.idxmax()}\n\n"
        f"Sales: ₹{monthly_sales.max():,.2f}"
    )

st.divider()

# ---------- AI BUSINESS EXPLANATION ----------
st.subheader("🤖 AI Business Explanation")

if st.button(
    "✨ Generate Business Explanation",
    type="primary",
    key="generate_business_explanation"
):
    try:
        summary = (
            f"Total sales: ₹{total_sales:,.2f}. "
            f"Top category: {category_sales.idxmax()}, "
            f"sales ₹{category_sales.max():,.2f}. "
            f"Top region: {region_sales.idxmax()}, "
            f"sales ₹{region_sales.max():,.2f}. "
            f"Best sales month: {monthly_sales.idxmax()}, "
            f"sales ₹{monthly_sales.max():,.2f}. "
            f"Top product: {product_sales.idxmax()}, "
            f"sales ₹{product_sales.max():,.2f}."
        )

        with st.spinner("Generating business explanation..."):
            explanation = generate_explanation(
                "Explain the overall sales performance and provide "
                "actionable business recommendations.",
                summary
            )

        st.markdown(explanation)

    except Exception as error:
        st.error(f"Could not generate explanation: {error}")

st.divider()

# ---------- ASK YOUR AI SALES ANALYST ----------
st.header("🤖 Ask Your AI Sales Analyst")
st.caption(
    "Ask questions about your sales data and get results "
    "with a simple business explanation."
)



# ---------- SUGGESTED QUESTIONS ----------
st.markdown("**Try a question:**")

suggestions = [
    "Which region has the lowest sales?",
    "What is the best category?",
    "Show the top 5 products.",
    "Compare sales across categories.",
    "How many orders are there?"
]

if "ai_question_input" not in st.session_state:
    st.session_state["ai_question_input"] = ""

def select_question(question):
    st.session_state["ai_question_input"] = question

col1, col2, col3 = st.columns(3)

for i, suggestion in enumerate(suggestions):
    with [col1, col2, col3][i % 3]:
        st.button(
            suggestion,
            key=f"ai_question_button_{i}",
            use_container_width=True,
            on_click=select_question,
            args=(suggestion,)
        )

question = st.text_input(
    "Your question",
    key="ai_question_input",
    placeholder="Example: Which region has the lowest sales?"
)

# ---------- ANALYZE QUESTION ----------
if st.button("Analyze", type="primary", key="ask_ai_analyze"):
    question = st.session_state["ai_question_input"]

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Analyzing your sales data..."):
                plan = interpret_question(question)
                result = execute_analysis(plan)

            st.markdown("### 📌 Analysis Result")
            st.success(str(result))

            with st.spinner("Generating business explanation..."):
                explanation = generate_explanation(question, result)

            st.markdown("### 💡 Business Explanation")
            st.write(explanation)

        except Exception as error:
            st.error(f"Analysis failed: {error}")

# ---------- AI BUSINESS RECOMMENDATIONS ----------
st.divider()
st.subheader("🎯 AI Business Recommendations")

best_category = category_sales.idxmax()
best_region = region_sales.idxmax()
lowest_region = region_sales.idxmin()
best_product = product_sales.idxmax()
best_month = monthly_sales.idxmax()
lowest_month = monthly_sales.idxmin()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📦 Category Strategy")
    st.write(
        f"Focus on the **{best_category}** category, "
        "which has the highest sales. Review its product "
        "performance to identify opportunities for growth."
    )

    st.markdown("#### 🌍 Regional Strategy")
    st.write(
        f"The **{best_region}** region leads in sales. "
        f"Investigate opportunities to improve performance "
        f"in the **{lowest_region}** region."
    )

with col2:
    st.markdown("#### 📅 Monthly Sales Strategy")
    st.write(
        f"Sales were highest in **{best_month}** and lowest "
        f"in **{lowest_month}**. Investigate seasonal trends "
        "and plan campaigns for weaker periods."
    )

    st.markdown("#### 🏆 Product Strategy")
    st.write(
        f"**{best_product}** is the top-selling product. "
        "Monitor its demand and stock availability when "
        "planning inventory and promotions."
    )

# ---------- DATA PREVIEW ----------
with st.expander("View sales dataset"):
    st.dataframe(df, use_container_width=True)
