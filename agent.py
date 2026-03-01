from monday_api import fetch_board_items
from data_cleaning import (
    items_to_dataframe,
    clean_numeric,
    normalize_sector,
    map_probability_labels,
)
from analytics import (
    sector_pipeline_insight,
    pipeline_summary,
    detect_sector_from_question,
    strongest_sector,
    sector_health_metrics,
)


def run_query(question):
    trace = []

    trace.append("Fetching Deals board")
    deals_items = fetch_board_items("Deals")
    deals_df = items_to_dataframe(deals_items)

    deals_df = clean_numeric(deals_df, "Deal Value")
    deals_df = normalize_sector(deals_df)

    # map Closure Probability labels → numeric
    deals_df = map_probability_labels(deals_df, "Closure Probability")

    q = question.lower()
    sector = detect_sector_from_question(question, deals_df)

    # ✅ NEW: check if detected sector exists in data
    if sector:
        available_sectors = set(
            deals_df["Sector"].dropna().str.lower().unique()
        )

        if sector.lower() not in available_sectors:
            answer = (
                f"No '{sector}' sector deals found in current pipeline. "
                f"Available sectors: {', '.join(sorted(s.title() for s in available_sectors))}."
            )
            trace.append(f"Sector '{sector}' not found")
            return answer, trace

    # strongest / biggest / largest sector
    if "strongest" in q or "biggest" in q or "largest" in q:
        s, val = strongest_sector(deals_df)
        if s:
            answer = f"{s} is currently the largest sector with pipeline value {val:.0f}."
        else:
            answer = "Unable to determine strongest sector."
        trace.append("Computed strongest sector")
        return answer, trace

    # sector-specific analysis
    if sector:
        insight = sector_pipeline_insight(deals_df, sector)
        health = sector_health_metrics(deals_df, sector)
        trace.append(f"Detected sector: {sector}")

        rank = insight["rank"]
        share = insight["share"] * 100
        strength = insight["strength"]

        answer = (
            f"{sector} pipeline appears {strength}, ranking #{rank} "
            f"and contributing {share:.1f}% of total value."
        )

        if health["late_ratio"] is not None:
            answer += f" {health['late_ratio']*100:.0f}% of deals are in late stages."

        if health["weighted_value"] is not None:
            answer += f" Expected revenue ≈ {health['weighted_value']:.0f}."

        if health["prob_missing"] is not None and health["prob_missing"] > 0:
            answer += f" Probability missing for {health['prob_missing']*100:.0f}% of deals."

        return answer, trace

    # overall pipeline fallback
    total_count, total_value, _ = pipeline_summary(deals_df)
    trace.append("Computed overall pipeline")

    answer = f"Overall pipeline: {total_count} deals worth {total_value:.0f}."
    return answer, trace