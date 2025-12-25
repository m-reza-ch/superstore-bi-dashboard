import streamlit as st
import plotly.express as px

from src.data_cleaning import load_and_clean
from src.features import add_time_features
from src.analytics import *
from src.charts import *
from src.insights import *

st.set_page_config(page_title="Superstore BI", layout="wide")
st.markdown(
    "<h1 style='text-align:center'>Superstore BI Dashboard</h1>",
    unsafe_allow_html=True,
)

df = add_time_features(load_and_clean("data/superstore_raw.csv"), "Order Date")

# KPI BAR (always visible)
k = kpis(df)
c1, c2, c3, c4, c5 = st.columns(5)
sales_delta = calculate_delta(df, "Sales")
c1.metric("Revenue", f"${k['Total Sales']:,}", f"{sales_delta:.1f}%")
c2.metric("Profit", f"${k['Total Profit']:,}")
c3.metric("Orders", k["Orders"])
c4.metric("Customers", k["Customers"])
c5.metric("Avg Order", f"${k['Avg Order Value']:,}")

with st.expander("Data Health Monitor"):
    health = []
    health.append(f"Missing values: `{df.isnull().sum().sum()}`")
    health.append(f"Duplicate rows: `{df.duplicated().sum()}`")
    health.append(f"Rows: `{len(df)}`")
    for h in health:
        st.markdown(f"{h}")

with st.expander("Automated Business Insights"):
    for i in generate_insights(df):
        st.markdown(f"{i}")


# GRID ROW 1
r1_l, r1_r = st.columns([1.5, 1])

with r1_l:
    with st.expander("Sales Trend", expanded=True):
        st.plotly_chart(trend_chart(sales_trend(df)), use_container_width=True)

with r1_r:
    with st.expander("Geographic Performance", expanded=True):
        st.plotly_chart(geo_sales_map(df), use_container_width=True)

# GRID ROW 2
r2_l, r2_r = st.columns(2)

with r2_l:
    with st.expander("Segment & Regional Comparison", expanded=True):
        st.plotly_chart(
            comparison_chart(
                sales_by_segment_category(df),
                SEGMENT_COL,
                SALES_COL,
                title="Sales by Segment and Category",
            ),
            use_container_width=True,
        )

        st.plotly_chart(
            comparison_chart(
                sales_by_region_category(df),
                REGION_COL,
                SALES_COL,
                title="Sales by Region and Category",
            ),
            use_container_width=True,
        )

with r2_r:
    with st.expander("Product Intelligence", expanded=True):
        st.plotly_chart(
            px.bar(top_products(df), x="Product Name", y="Sales"),
            use_container_width=True,
        )
        st.plotly_chart(
            px.bar(loss_products(df), x="Product Name", y="Profit"),
            use_container_width=True,
        )

with st.expander("Correlation & Relationships", expanded=True):
    c1, c2 = st.columns(2)

    c1.plotly_chart(correlation_heatmap(df), use_container_width=True)

    c2.plotly_chart(
        relationship_chart(quantity_vs_profit(df)), use_container_width=True
    )

with st.expander("Sales & Profit Distribution", expanded=True):
    c1, c2 = st.columns(2)

    c1.plotly_chart(donut_sales_by_segment(df), use_container_width=True)

    c2.plotly_chart(donut_profit_by_category(df), use_container_width=True)
