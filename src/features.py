def add_time_features(df, date_col):
    df["Month"] = df[date_col].dt.to_period("M").dt.to_timestamp()
    df["Year"] = df[date_col].dt.year
    return df
