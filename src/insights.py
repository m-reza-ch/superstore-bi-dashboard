import numpy as np
import pandas as pd


def generate_insights(df):
    insights = []

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    orders = df["Order ID"].nunique()
    avg_order = total_sales / orders

    # Profit margin
    margin = (total_profit / total_sales) * 100

    # Regional performance
    region_sales = df.groupby("Region")["Sales"].sum()
    region_profit = df.groupby("Region")["Profit"].sum()

    top_region = region_sales.idxmax()
    worst_region = region_profit.idxmin()

    # Category performance
    cat_profit = df.groupby("Category")["Profit"].sum()
    top_category = cat_profit.idxmax()
    loss_category = cat_profit.idxmin()

    # Trend detection (last 6 vs previous 6 months)
    df["Month"] = df["Order Date"].dt.to_period("M")
    monthly_sales = df.groupby("Month")["Sales"].sum().sort_index()

    recent = monthly_sales.tail(6).mean()
    previous = monthly_sales.iloc[-12:-6].mean()
    growth = ((recent - previous) / previous) * 100 if previous > 0 else 0

    # Concentration risk
    top_products = (
        df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False)
    )
    top10_share = (top_products.head(10).sum() / total_sales) * 100

    # Insights
    insights.append(
        f"Total revenue is `${total_sales:,.0f}` with a profit of `${total_profit:,.0f}` (with `{margin:.1f}%` margin)."
    )
    insights.append(
        f"Average order value is `{avg_order:,.2f}` across `{orders}` orders."
    )
    insights.append(
        f"The `{top_region}` region is the strongest, and the `{worst_region}` region has the weakest revenue contributor and requires cost review."
    )
    insights.append(
        f"`{top_category}` is the most profitable category and the`{loss_category}` shows the highest loss risk."
    )
    insights.append(f"Sales growth over the last 6 months is `{growth:.1f}%`.")
    insights.append(
        f"Top 10 products generate `{top10_share:.1f}%` of total revenue (concentration risk indicator)."
    )

    # Executive recommendations
    if growth < 0:
        insights.append(
            "**Note**: Sales are declining recently. Marketing and pricing strategy review is recommended."
        )
    if margin < 15:
        insights.append(
            "**Note**: Overall profit margin is low. Cost optimization is recommended."
        )
    if top10_share > 50:
        insights.append(
            "**Note**: Revenue concentration is high. Product portfolio diversification is advised."
        )

    return insights


def calculate_delta(dataframe, column_name):
    """
    Calculates the % growth between the last month and the previous month
    for a specific column.
    """
    # Get the last two months sorted
    sorted_months = dataframe["Month"].sort_values().unique()

    # Safety check: Ensure we actually have 2 months of data
    if len(sorted_months) < 2:
        return 0

    current_m = sorted_months[-1]
    prev_m = sorted_months[-2]

    # Calculate sums
    curr_val = dataframe[dataframe["Month"] == current_m][column_name].sum()
    prev_val = dataframe[dataframe["Month"] == prev_m][column_name].sum()

    # Calculate Delta with zero-division protection
    if prev_val == 0:
        return 0
    return ((curr_val - prev_val) / prev_val) * 100
