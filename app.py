
import streamlit as st
import pandas as pd
import json
import urllib.request

from ai_engine import (
    df,
    interpret_question,
    execute_analysis,
    generate_explanation
)

st.set_page_config(
    page_title="AI Sales Analyst",
    page_icon="📊",
    layout="wide"
)

# ---------- SIDEBAR NAVIGATION STYLING ----------

st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }

    [data-testid="stSidebarNav"] ul {
        gap: 0.4rem;
    }

    [data-testid="stSidebarNav"] a {
        padding: 0.7rem 1rem;
        margin: 0.2rem 0.4rem;
        border-radius: 8px;
        min-height: 3rem;
        display: flex;
        align-items: center;
    }

    [data-testid="stSidebarNav"] a span {
        font-size: 1.05rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- PROFESSIONAL WHITE THEME ----------
st.markdown("""
<style>
.stApp {
    background-color: #f5f8fc;
    color: #1e293b;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #173b70;
}

[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #dbe5f1;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 7px rgba(30, 64, 120, 0.05);
}

[data-testid="stMetricLabel"] {
    color: #52657d;
}

[data-testid="stMetricValue"] {
    color: #174ea6;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1rem;
}

.stButton button:hover {
    background-color: #1d4ed8;
    color: white;
    border: none;
}

[data-testid="stTextInput"] input {
    border-radius: 8px;
    background-color: white;
}

[data-testid="stExpander"] {
    background-color: white;
    border: 1px solid #dbe5f1;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("📊 AI Sales Analyst")
st.caption(
    "Your intelligent sales assistant | "
    "Powered by Python, Ollama and Streamlit"
)

st.divider()

# ---------- KPI METRICS ----------

# ---------- INTERACTIVE FILTERS ----------
st.subheader("🔎 Filter Sales Data")

filter1, filter2, filter3 = st.columns(3)

with filter1:
    selected_categories = st.multiselect(
        "Category",
        options=sorted(df["Category"].dropna().unique()),
        default=sorted(df["Category"].dropna().unique())
    )

with filter2:
    selected_regions = st.multiselect(
        "Region",
        options=sorted(df["Region"].dropna().unique()),
        default=sorted(df["Region"].dropna().unique())
    )

with filter3:
    selected_statuses = st.multiselect(
        "Order Status",
        options=sorted(df["Order Status"].dropna().unique()),
        default=sorted(df["Order Status"].dropna().unique())
    )

filtered_df = df[
    df["Category"].isin(selected_categories)
    & df["Region"].isin(selected_regions)
    & df["Order Status"].isin(selected_statuses)
]

st.caption(f"Showing {len(filtered_df)} of {len(df)} records.")
st.divider()

total_sales = filtered_df["Sales Amount"].sum()
total_quantity = filtered_df["Quantity"].sum()
average_sales = filtered_df["Sales Amount"].mean()
total_orders = filtered_df["Order ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("📦 Quantity Sold", f"{total_quantity:,}")
col3.metric(
    "🧾 Average Sale",
    f"₹{average_sales:,.2f}" if pd.notna(average_sales) else "₹0.00"
)
col4.metric("🛒 Total Orders", f"{total_orders:,}")

st.divider()

# ---------- SALES OVERVIEW ----------
st.subheader("📈 Sales Overview")
st.caption("Explore sales performance across categories and regions.")

left, right = st.columns(2)

with left:
    st.markdown("**Sales by Category**")
    category_sales = (
        df.groupby("Category")["Sales Amount"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(category_sales, color="#3b82f6")

with right:
    st.markdown("**Sales by Region**")
    region_sales = (
        df[df["Region"] != "Not given"]
        .groupby("Region")["Sales Amount"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(region_sales, color="#14b8a6")

# ---------- SALES DISTRIBUTION PIE CHART ----------
st.markdown("### 🥧 Sales Distribution by Category")
st.caption("Understand each category's contribution to total sales.")

pie_data = (
    df.groupby("Category", as_index=False)["Sales Amount"]
    .sum()
    .rename(columns={"Sales Amount": "Sales"})
)

pie_col1, pie_col2, pie_col3 = st.columns([1, 2, 1])

with pie_col2:
    st.vega_lite_chart(
        pie_data,
        {
            "mark": {"type": "arc", "outerRadius": 130},
            "encoding": {
                "theta": {
                    "field": "Sales",
                    "type": "quantitative"
                },
                "color": {
                    "field": "Category",
                    "type": "nominal",
                    "legend": {"title": "Category"}
                },
                "tooltip": [
                    {"field": "Category", "type": "nominal"},
                    {
                        "field": "Sales",
                        "type": "quantitative",
                        "format": ",.2f"
                    }
                ]
            },
            "view": {"stroke": None}
        },
        use_container_width=True
    )

# ---------- MONTHLY SALES TREND ----------
st.divider()

st.subheader("📈 Monthly Sales Trend")
st.caption("Track how total sales change from month to month.")

monthly_sales = (
    df.groupby("Month")["Sales Amount"]
    .sum()
    .sort_index()
)

st.line_chart(
    monthly_sales,
    color="#2563eb",
    x_label="Month",
    y_label="Sales Amount (₹)"
)


# ---------- SALES GROWTH AND COMPARISON ----------
st.divider()

st.subheader("📊 Sales Growth & Comparison")
st.caption(
    "Compare monthly sales and track percentage changes "
    "using your selected filters."
)

if filtered_df.empty:
    st.info("No data available for the selected filters.")
else:
    # Calculate monthly sales in chronological order

    # Calculate monthly sales in chronological order
    monthly_comparison = (
        filtered_df.groupby(["Month", "Month Name"])["Sales Amount"]
        .sum()
        .reset_index()
        .sort_values("Month")
        .reset_index(drop=True)
    )

    # Check whether each month exists in the filtered data
    monthly_comparison["Previous Month Sales"] = (
        monthly_comparison["Sales Amount"].shift(1)
    )

    previous_sales = monthly_comparison["Previous Month Sales"]

    # Avoid division by zero
    monthly_comparison["Growth (%)"] = (
        (monthly_comparison["Sales Amount"] - previous_sales)
        / previous_sales.replace(0, float("nan"))
    ) * 100

    expected_months = {1, 2, 3, 4, 5, 6}
    available_months = set(monthly_comparison["Month"].dropna())

    missing_months = expected_months - available_months

    if missing_months:
        st.warning(
            "Some months are missing from the filtered data. "
            "Growth compares consecutive available months."
        )

    # Latest available month comparison
    if len(monthly_comparison) >= 2:
        current = monthly_comparison.iloc[-1]
        previous = monthly_comparison.iloc[-2]

        current_sales = current["Sales Amount"]
        previous_month_sales = previous["Sales Amount"]
        current_month = current["Month Name"]
        previous_month = previous["Month Name"]

        growth = current["Growth (%)"]

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Latest Month",
            str(current_month)
        )

        metric2.metric(
            f"{current_month} Sales",
            f"₹{current_sales:,.2f}"
        )

        if pd.notna(growth):
            metric3.metric(
                "Growth vs Previous Month",
                f"{growth:+.2f}%",
                delta=f"{growth:+.2f}%"
            )
        else:
            metric3.metric(
                "Growth vs Previous Month",
                "N/A"
            )

        st.caption(
            f"Comparing {current_month} with {previous_month}. "
            "The comparison uses the latest two months available "
            "in the filtered data."
        )
    else:
        st.info(
            "At least two months of data are needed to calculate "
            "monthly sales growth."
        )

    # Detailed monthly comparison table
    st.markdown("#### 📋 Monthly Comparison Table")

    display_comparison = monthly_comparison[
        [
            "Month Name",
            "Sales Amount",
            "Previous Month Sales",
            "Growth (%)"
        ]
    ].copy()

    display_comparison = display_comparison.rename(
        columns={
            "Month Name": "Month",
            "Sales Amount": "Sales (₹)",
            "Previous Month Sales": "Previous Sales (₹)",
            "Growth (%)": "Growth (%)"
        }
    )

    st.dataframe(
        display_comparison,
        use_container_width=True,
        hide_index=True
    )

    # Visualize month-over-month growth
    
    growth_chart = monthly_comparison.dropna(
        subset=["Growth (%)"]
    ).sort_values("Month").copy()

    if not growth_chart.empty:
        st.markdown("#### 📈 Monthly Sales Growth (%)")
        st.bar_chart(
            growth_chart,
            x="Month Name",
            y="Growth (%)",
            sort=False,
            color="#14b8a6",
            x_label="Month",
            y_label="Growth (%)"
        )


# ---------- TOP 5 PRODUCTS ----------
st.divider()

st.subheader("🏆 Top 5 Products by Sales")
st.caption("Discover which products generate the highest sales.")

top_products = (
    df.groupby("Product")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .sort_values(ascending=True)
)

st.bar_chart(
    top_products,
    color="#8b5cf6",
    x_label="Sales Amount (₹)",
    y_label="Product",
    horizontal=True
)

st.divider()

st.subheader("📦 Order Status Analysis")
st.caption(
    "Monitor completed orders, returns, cancellations and pending orders."
)

if filtered_df.empty:
    st.info("No records match your selected filters.")
else:
    # Count unique orders for each status
    
    duplicate_status_orders = (
        filtered_df.groupby("Order ID")["Order Status"].nunique()
    )

    st.write(
        "Orders with multiple statuses:",
        int((duplicate_status_orders > 1).sum())
    )

    status_names = ["Delivered", "Returned", "Cancelled", "Pending"]

    status_counts = (
        filtered_df.groupby("Order Status")["Order ID"]
        .nunique()
        .reindex(status_names, fill_value=0)
    )

    total_orders_status = filtered_df["Order ID"].nunique()

    cancelled_orders = int(status_counts["Cancelled"])
    returned_orders = int(status_counts["Returned"])

    # Calculate rates
    cancellation_rate = (
        cancelled_orders / total_orders_status * 100
        if total_orders_status else 0
    )

    return_rate = (
        returned_orders / total_orders_status * 100
        if total_orders_status else 0
    )

    # Display status counts
    st.markdown("#### 📊 Order Counts")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("✅ Delivered", f"{status_counts['Delivered']:,}")
    c2.metric("↩️ Returned", f"{returned_orders:,}")
    c3.metric("❌ Cancelled", f"{cancelled_orders:,}")
    c4.metric("⏳ Pending", f"{status_counts['Pending']:,}")

    st.markdown("#### 📉 Cancellation & Return Rates")

    r1, r2 = st.columns(2)

    r1.metric(
        "Cancellation Rate",
        f"{cancellation_rate:.2f}%"
    )

    r2.metric(
        "Return Rate",
        f"{return_rate:.2f}%"
    )

    # Visualize counts by status
    st.markdown("#### 📊 Orders by Status")

    st.bar_chart(
        status_counts,
        color="#3b82f6",
        x_label="Order Status",
        y_label="Number of Orders"
    )

    # Show detailed table
    status_table = status_counts.rename("Number of Orders").reset_index()
    status_table.columns = ["Order Status", "Number of Orders"]

    st.dataframe(
        status_table,
        use_container_width=True,
        hide_index=True
    )
# ---------- AUTOMATIC BUSINESS INSIGHTS ----------


# ---------- ORDER STATUS ANALYSIS ----------


# ---------- DOWNLOAD SALES REPORT ----------
st.divider()
st.subheader("📥 Download Sales Report")
st.caption("Export the sales records matching your selected filters.")

if filtered_df.empty:
    st.info("No records available to download. Please adjust your filters.")
else:
    csv_data = filtered_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Download Filtered Sales Report",
        data=csv_data,
        file_name="AI_Sales_Analyst_Report.csv",
        mime="text/csv",
        type="primary"
    )

# ---------- DATA PREVIEW ----------
with st.expander("📂 View Sales Dataset"):
    st.write(
        f"Dataset contains {len(df)} rows and "
        f"{len(df.columns)} columns."
    )
    st.dataframe(df, use_container_width=True)
