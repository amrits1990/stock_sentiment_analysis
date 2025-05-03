import pandas as pd

def get_index_constituents(index_name):
    index_name = index_name.strip().upper()

    sources = {
        "NIFTY 50": "https://en.wikipedia.org/wiki/NIFTY_50",
        "SENSEX": "https://en.wikipedia.org/wiki/BSE_SENSEX",
        "NIFTY 500": "https://en.wikipedia.org/wiki/NIFTY_500",
        "BANK NIFTY": "https://en.wikipedia.org/wiki/NIFTY_Bank"
    }

    if index_name not in sources:
        raise ValueError(f"Unsupported index '{index_name}'. Choose from {list(sources.keys())}")

    url = sources[index_name]
    print(f"Fetching constituents for {index_name} from Wikipedia...")

    tables = pd.read_html(url)

    candidates = []
    for table in tables:
        # Flatten MultiIndex columns (if any)
        if isinstance(table.columns, pd.MultiIndex):
            table.columns = [' '.join(col).strip() for col in table.columns.values]
        else:
            table.columns = table.columns.astype(str)

        cols = [col.lower() for col in table.columns]
        if any('symbol' in col or 'ticker' in col for col in cols):
            candidates.append(table)

    if not candidates:
        raise Exception("Couldn't find constituents table.")

    df = candidates[0]

    possible_cols = [col for col in df.columns if 'symbol' in col.lower() or 'ticker' in col.lower() or 'code' in col.lower()]
    symbols = df[possible_cols[0]].dropna().unique().tolist()

    return symbols