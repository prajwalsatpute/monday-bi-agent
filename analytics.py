import pandas as pd


def detect_sector_from_question(question, deals_df):
    if "sector" not in question.lower():
        # still try to match known sectors
        sectors = deals_df["Sector"].dropna().unique()
        q = question.lower()
        for s in sectors:
            if str(s).lower() in q:
                return s
        return None

    # if user explicitly mentions a sector-like word
    words = question.lower().split()

    # known sectors
    known = [str(s).lower() for s in deals_df["Sector"].dropna().unique()]

    for w in words:
        if w in known:
            return w

    # return possible sector even if unknown
    # e.g. healthcare, telecom, etc.
    for w in words:
        if w not in ["sector", "pipeline", "how", "is", "are", "we", "have"]:
            return w

    return None


def pipeline_summary(deals_df):
    total_value = deals_df["Deal Value"].sum()
    total_count = len(deals_df)

    by_sector = (
        deals_df.groupby("Sector")["Deal Value"]
        .sum()
        .sort_values(ascending=False)
    )

    return total_count, total_value, by_sector


def sector_pipeline_insight(deals_df, sector):
    df = deals_df[deals_df["Sector"].str.contains(sector, case=False, na=False)]

    sector_value = df["Deal Value"].sum()
    sector_count = len(df)
    avg_prob = df["Probability_Num"].mean()

    total_count, total_value, by_sector = pipeline_summary(deals_df)

    share = sector_value / total_value if total_value > 0 else 0

    rank = (
        list(by_sector.index).index(sector) + 1
        if sector in by_sector.index
        else None
    )

    if share > 0.4:
        strength = "very strong"
    elif share > 0.25:
        strength = "strong"
    elif share > 0.15:
        strength = "moderate"
    else:
        strength = "weak"

    return {
        "sector_count": sector_count,
        "sector_value": sector_value,
        "avg_prob": avg_prob,
        "share": share,
        "rank": rank,
        "strength": strength,
        "total_value": total_value,
    }


def sector_health_metrics(deals_df, sector):
    df = deals_df[deals_df["Sector"].str.contains(sector, case=False, na=False)].copy()

    if "Stage" in df.columns:
        late_stages = df["Stage"].str.contains(
            "proposal|negotiation|order|won",
            case=False,
            na=False,
        )
        late_ratio = late_stages.mean()
    else:
        late_ratio = None

    if "Probability_Num" in df.columns:
        weighted = (df["Deal Value"] * df["Probability_Num"] / 100).sum()
        prob_missing = df["Probability_Num"].isna().mean()
    else:
        weighted = None
        prob_missing = None

    return {
        "late_ratio": late_ratio,
        "weighted_value": weighted,
        "prob_missing": prob_missing,
    }


def strongest_sector(deals_df):
    _, _, by_sector = pipeline_summary(deals_df)
    if len(by_sector) == 0:
        return None, None
    return by_sector.index[0], by_sector.iloc[0]