import plotly.express as px
from src.config import *
from src.analytics import *


def trend_chart(df):
    return px.line(df, x="Month", y=SALES_COL, title="Monthly Sales Trend")


def comparison_chart(df, x, y, title):
    return px.bar(
        df,
        x=x,
        y=y,
        color=CATEGORY_COL,
        barmode="group",
        title=title,
    )


def histogram_distribution(df):
    return px.histogram(
        df,
        x=[SALES_COL],
        nbins=50,
        title="Sales Value Distribution (Histogram)",
    )


def boxplot_distribution(df):
    return px.box(df, y=SALES_COL, title="Sales Distribution (Box Plot)")


def treemap_composition(df):
    return px.treemap(
        df, path=[CATEGORY_COL], values=SALES_COL, title="Sales Share by Category"
    )


def relationship_chart(df):
    return px.scatter(
        df,
        x=QUANTITY_COL,
        y=PROFIT_COL,
        color=CATEGORY_COL,
        title="Quantity vs Profit Relationship",
    )


def correlation_heatmap(df):
    corr = df[["Sales", "Profit", "Quantity", "Discount"]].corr()
    return px.imshow(corr, text_auto=True, title="Feature Correlation Matrix")


def geo_sales_map(df):
    geo = geo_sales(df)

    return px.choropleth(
        geo,
        locations="Code",
        locationmode="USA-states",
        color="Sales",
        hover_name="Label",  # 👈 full readable name
        hover_data={"Sales": ":,.0f"},
        scope="usa",
        title="Sales by U.S. State",
    )


def donut_sales_by_segment(df):
    seg = df.groupby("Segment")["Sales"].sum().reset_index()
    return px.pie(
        seg, names="Segment", values="Sales", hole=0.45, title="Sales Share by Segment"
    )


def donut_profit_by_category(df):
    cat = df.groupby("Category")["Profit"].sum().reset_index()
    return px.pie(
        cat,
        names="Category",
        values="Profit",
        hole=0.45,
        title="Profit Share by Category",
    )
