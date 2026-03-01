import json
import pandas as pd


def items_to_dataframe(items):
    rows = []

    for item in items:
        row = {"Deal Name": item["name"]}

        for col in item["column_values"]:
            title = col["column"]["title"]
            text = col.get("text")
            value = col.get("value")

            if text:
                row[title] = text
            elif value:
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, dict) and "number" in parsed:
                        row[title] = parsed["number"]
                    else:
                        row[title] = None
                except:
                    row[title] = None
            else:
                row[title] = None

        rows.append(row)

    return pd.DataFrame(rows)


def clean_numeric(df, col):
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def normalize_sector(df):
    if "Sector" in df.columns:
        df["Sector"] = (
            df["Sector"]
            .astype(str)
            .str.strip()
            .str.title()
        )
    return df


def map_probability_labels(df, col="Closure Probability"):
    if col not in df.columns:
        return df

    mapping = {
        "low": 25,
        "medium": 50,
        "high": 75,
        "won": 100,
    }

    df["Probability_Num"] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(mapping)
    )

    return df