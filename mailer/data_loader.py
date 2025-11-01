import pandas as pd

def load_data(path):
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    print(f"Loaded {len(df)} rows from {path}")
    return df