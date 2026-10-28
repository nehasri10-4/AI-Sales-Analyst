
import os
import streamlit as st

st.set_page_config(
    page_title="Power BI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------- POWER BI PAGE ----------
st.title("📊 Power BI Dashboard")
st.caption(
    "Explore your sales report with interactive Power BI charts, "
    "filters, and slicers."
)

POWER_BI_FILE = r"D:\AI sales Analysis\Dashboard.pbix"

st.divider()

st.subheader("Your Interactive Sales Report")

st.write(
    "Open your Power BI report in Power BI Desktop to explore "
    "the complete dashboard and interact with its slicers."
)

if st.button(
    "🚀 Open Power BI Dashboard",
    type="primary",
    use_container_width=True
):
    if os.path.isfile(POWER_BI_FILE):
        try:
            os.startfile(POWER_BI_FILE)
            st.success(
                "Your Power BI report has been opened. "
                "You can now use its interactive filters and slicers."
            )
        except OSError as error:
            st.error(f"Could not open the Power BI report: {error}")
    else:
        st.error(
            f"Power BI report not found at:\n{POWER_BI_FILE}\n\n"
            "Check that the file exists and that its name is correct."
        )

st.divider()

st.caption(
    "Note: This local integration opens Power BI Desktop. "
    "The report is not embedded inside this Streamlit page."
)
