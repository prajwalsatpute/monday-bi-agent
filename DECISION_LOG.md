# Monday.com Business Intelligence Agent – Decision Log
## Overview
The goal was to build a conversational business intelligence agent capable of answering founder-level questions using messy monday.com Deals and Work Orders data. The primary challenge involved interpreting natural language queries, cleaning inconsistent business data, and generating meaningful pipeline insights in real time.

## Architecture Decisions
The agent uses a lightweight Streamlit interface connected to a Python analytics layer. Queries trigger live monday.com GraphQL API calls at runtime, ensuring up-to-date results without caching.

#### Architecture flow:

User → Streamlit → Agent → monday API → Data Cleaning → Analytics → Answer

This structure separates concerns between data retrieval, cleaning, analytics, and presentation.

## monday.com Integration

Live API integration was chosen over exports or caching to satisfy assignment requirements. Each query fetches board data dynamically using monday’s GraphQL API.

Only relevant boards are queried at runtime, ensuring correctness and freshness of insights.

## Handling Messy Data

The provided data contained inconsistent probability formats (categorical labels), missing values, and numeric formatting issues.

#### Decisions:

- Closure Probability converted to Status column in monday
- Labels mapped to numeric probabilities (High=75, Medium=50, Low=25)
- Numeric cleaning applied to deal values
- Sector names normalized
- Missing probability explicitly surfaced in answers

This ensures analytics remain valid despite incomplete data.

## Business Intelligence Logic

The agent provides sector-level pipeline insights aligned with executive decision needs:
- Pipeline value aggregation
- Sector contribution share
- Sector ranking
- Pipeline strength classification
- Late-stage maturity ratio
- Expected revenue (probability-weighted)
- Data quality caveats

#### Strength classification thresholds were chosen to reflect practical pipeline interpretation:
- 40% share → very strong
- 25–40% → strong
- 15–25% → moderate
- <15% → weak

## Query Understanding

Sector detection is performed by matching query terms against available sectors. Unknown sectors are handled gracefully by informing the user and listing available sectors.

#### Keyword intent detection supports:
- strongest / biggest sector
- pipeline health
- reliability questions
- sector performance

This covers typical founder-level BI queries.

## Agent Trace Visibility

The agent exposes internal steps (e.g., fetching boards, detecting sector) to ensure transparency and trust in automated analysis, as required by the assignment.

## Deployment

The agent is deployed on Render to provide a public, no-setup prototype. The monday API token is injected via environment variables to maintain security.

## Limitations & Future Improvements
- Cross-board analytics currently focused on Deals board
- Follow-up conversational memory not implemented
- Clarification prompts minimal

These can be extended by linking Work Orders metrics to pipeline insights.

## Conclusion

The final agent satisfies assignment goals by combining live monday integration, messy data normalization, and actionable BI insights in a conversational interface suitable for executive decision support.