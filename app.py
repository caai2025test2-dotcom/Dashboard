import streamlit as st
import plotly.express as px
from data_processing import load_and_clean_data

st.set_page_config(page_title="Deficiency Dashboard", layout="wide")

DATA_PATH = "data/deficiency_data.xlsx"
df = load_and_clean_data(DATA_PATH)

# --- Sidebar Filters ---
st.sidebar.header("Filters")

year_filter = st.sidebar.multiselect(
    "Year",
    options=sorted(df["year"].dropna().unique()),
    default=sorted(df["year"].dropna().unique())
)

segment_filter = st.sidebar.multiselect(
    "Business Segment",
    options=df["business_segment"].dropna().unique(),
    default=df["business_segment"].dropna().unique()
)

filtered_df = df[
    (df["year"].isin(year_filter)) &
    (df["business_segment"].isin(segment_filter))
]

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Issues", len(filtered_df))
col2.metric("Issues This Year", len(filtered_df[filtered_df["year"] == df["year"].max()]))
col3.metric("Avg Days Open", int(filtered_df["days_open"].mean()))
col4.metric("High Risk Issues", len(filtered_df[filtered_df["issue_classification"] == "High"]))

# --- Charts ---
st.markdown("### Trends")

fig_time = px.histogram(
    filtered_df,
    x="creation_date",
    nbins=12,
    title="Issues Over Time"
)
st.plotly_chart(fig_time, use_container_width=True)

col5, col6 = st.columns(2)

fig_segment = px.bar(
    filtered_df,
    x="business_segment",
    title="Issues by Business Segment"
)
col5.plotly_chart(fig_segment, use_container_width=True)

fig_location = px.bar(
    filtered_df,
    x="location",
    title="Issues by Location"
)
col6.plotly_chart(fig_location, use_container_width=True)

# --- Aging ---
st.markdown("### Aging Analysis")
fig_aging = px.bar(
    filtered_df,
    x="aging_bucket",
    title="Issue Aging"
)
st.plotly_chart(fig_aging, use_container_width=True)

# --- Table ---
st.markdown("### Issue Details")
st.dataframe(
    filtered_df.sort_values("days_open", ascending=False),
    use_container_width=True
)
