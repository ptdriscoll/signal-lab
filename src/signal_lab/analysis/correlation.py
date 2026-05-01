def compute(df, col_a, col_b):
    return df[col_a].corr(df[col_b])
