from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd
from src.config import *


# TREND
def sales_trend(df):
    trend = df.groupby("Month")["Sales"].sum().reset_index()
    trend["Month"] = trend["Month"].dt.to_timestamp()  # 👈 correct
    return trend


# COMPARISON
def sales_by_region_category(df):
    return df.groupby([REGION_COL, CATEGORY_COL])[SALES_COL].sum().reset_index()


def sales_by_segment_category(df):
    return df.groupby([SEGMENT_COL, CATEGORY_COL])[SALES_COL].sum().reset_index()


# DISTRIBUTION
def sales_distribution(df):
    return df.groupby(CATEGORY_COL)[SALES_COL].sum().reset_index()


# RELATIONSHIP
def quantity_vs_profit(df):
    return df[[QUANTITY_COL, PROFIT_COL, CATEGORY_COL]]


# KPIs
def kpis(df):
    return {
        "Total Sales": round(df["Sales"].sum(), 2),
        "Total Profit": round(df["Profit"].sum(), 2),
        "Orders": df["Order ID"].nunique(),
        "Customers": df["Customer ID"].nunique(),
        "Avg Order Value": round(df["Sales"].sum() / df["Order ID"].nunique(), 2),
    }


# Additional Analytics
def profit_by_region(df):
    return df.groupby("Region")["Profit"].sum().reset_index()


def profit_by_category(df):
    return df.groupby("Category")["Profit"].sum().reset_index()


def loss_products(df):
    return (
        df.groupby("Product Name")["Profit"]
        .sum()
        .reset_index()
        .sort_values("Profit")
        .head(10)
    )


def top_products(df):
    return (
        df.groupby("Product Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
        .head(10)
    )


def segment_performance(df):
    return df.groupby("Segment")[["Sales", "Profit"]].sum().reset_index()


# FORECASTING
def sales_forecast(df, periods=6):
    ts = df.groupby("Month")["Sales"].sum()

    model = ExponentialSmoothing(ts, trend="add")
    fit = model.fit()
    forecast = fit.forecast(periods)

    forecast = forecast.reset_index()
    forecast.columns = ["Month", "Forecast"]
    forecast["Month"] = forecast["Month"].dt.to_timestamp()  # 👈 correct

    return forecast


STATE_ABBREV = {
    "Alabama": "AL",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}


def geo_sales(df):
    geo = df.groupby("State")["Sales"].sum().reset_index()
    geo["Code"] = geo["State"].map(STATE_ABBREV)
    geo["Label"] = geo["State"] + " (" + geo["Code"] + ")"
    return geo.dropna()
