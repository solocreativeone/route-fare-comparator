from pathlib import Path

import pandas as pd
import streamlit as st

from calculator import compare_routes, monthly_cost

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "fares.csv"

st.set_page_config(page_title="Route Fare Comparator", page_icon="🚌", layout="wide")
st.title("🚌 Route Fare Comparator")
st.caption("Compare transport fare estimates and plan your commute.")

@st.cache_data
def load_fares(path: Path) -> pd.DataFrame:
    """Load the shared fare dataset."""
    return pd.read_csv(path)

try:
    fares = load_fares(DATA_PATH)
except FileNotFoundError:
    st.error("Could not find data/fares.csv. Check the repository structure.")
    st.stop()

if fares.empty:
    st.warning("The fare dataset is empty. Add records to data/fares.csv.")
    st.stop()

required_columns = {
    "origin", "destination", "mode", "min_fare", "max_fare",
    "duration_min", "source", "date_collected"
}
missing = required_columns - set(fares.columns)
if missing:
    st.error(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    st.stop()

st.sidebar.header("Your journey")
origins = sorted(fares["origin"].dropna().astype(str).unique())
destinations = sorted(fares["destination"].dropna().astype(str).unique())

origin = st.sidebar.selectbox("From", origins)
destination_options = sorted(
    fares.loc[fares["origin"] == origin, "destination"].dropna().astype(str).unique()
)
destination = st.sidebar.selectbox(
    "To", destination_options if destination_options else destinations
)
trips_per_week = st.sidebar.number_input(
    "One-way trips per week", min_value=1, max_value=30, value=10, step=1
)
weeks_per_month = st.sidebar.number_input(
    "Weeks per month for estimate", min_value=1.0, max_value=5.0, value=4.33, step=0.1
)

if origin == destination:
    st.info("Choose different origin and destination locations.")
    st.stop()

results = compare_routes(fares, origin, destination)
if results.empty:
    st.warning("No fare records found for this route yet. Add data to data/fares.csv.")
    st.stop()

results = results.copy()
results["weekly_min"] = results["min_fare"] * trips_per_week
results["weekly_max"] = results["max_fare"] * trips_per_week
results["monthly_min"] = results["weekly_min"] * weeks_per_month
results["monthly_max"] = results["weekly_max"] * weeks_per_month

st.subheader(f"{origin} → {destination}")
st.caption("Estimates are based on the records currently in the shared dataset.")

left, right = st.columns(2)
with left:
    st.metric(
        "Lowest estimated one-way fare",
        f"₦{results['min_fare'].min():,.0f}"
    )
with right:
    st.metric(
        "Highest estimated one-way fare",
        f"₦{results['max_fare'].max():,.0f}"
    )

st.subheader("Fare options")
display = results[
    ["mode", "min_fare", "max_fare", "duration_min", "weekly_min",
     "weekly_max", "monthly_min", "monthly_max", "source", "date_collected"]
].rename(columns={
    "mode": "Transport mode",
    "min_fare": "Min one-way (₦)",
    "max_fare": "Max one-way (₦)",
    "duration_min": "Duration (min)",
    "weekly_min": "Weekly min (₦)",
    "weekly_max": "Weekly max (₦)",
    "monthly_min": "Monthly min (₦)",
    "monthly_max": "Monthly max (₦)",
    "source": "Source",
    "date_collected": "Date collected",
})
st.dataframe(display, use_container_width=True, hide_index=True)

st.subheader("Estimated monthly cost by transport mode")
chart_data = results.set_index("mode")[["monthly_min", "monthly_max"]].rename(
    columns={"monthly_min": "Monthly minimum", "monthly_max": "Monthly maximum"}
)
st.bar_chart(chart_data)

st.info(
    "Prototype note: sample records are illustrative and must be replaced with "
    "verified fares before presenting results as real-world estimates."
)
