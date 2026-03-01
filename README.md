# Monday.com Business Intelligence Agent

#### A conversational business intelligence agent that answers founder-level pipeline questions using live monday.com Deals and Work Orders boards.

#### The agent cleans messy business data, normalizes probability formats, and provides sector-level pipeline insights with transparent API traces.

## Live Demo
#### Hosted on [Render.com](https://render.com) with live monday API environment variable.

Host URL
👉 https://monday-bi-agent-xqfx.onrender.com


## Example questions:
- What is our overall pipeline?
- How is mining sector performing?
- Which sector has strongest pipeline?
- Do we have strong renewables pipeline?
- Are we overdependent on powerline?
- How reliable is renewables pipeline?
- How is healthcare sector pipeline?

## Monday Boards
- Deals board
👉 https://prajwalsatpute2000s-team.monday.com/boards/5026902623


- Work Orders board
👉 https://prajwalsatpute2000s-team.monday.com/boards/5026903022


## Features
- Live monday.com API integration (no caching)
- Handles messy probability labels (High/Medium/Low)
- Sector-level pipeline analytics
- Expected revenue estimation
- Pipeline strength classification
- Late-stage maturity analysis
- Data quality caveats
- Unknown sector handling
- Visible agent trace

## Architecture

#### User Question → Streamlit UI → Agent → monday API → Data Cleaning → Analytics → Answer + Trace

## Tech Stack
- Python
- Streamlit
- Pandas
- monday.com GraphQL API
- Render (deployment)

## Setup (Local)
```` bash git clone <repo>
cd monday-bi-agent
pip install -r requirements.txt
export MONDAY_API_TOKEN=your_token
streamlit run app.py
````

## Assignment Compliance

✔ Live monday integration

✔ Messy data handling

✔ Founder-level BI insights

✔ Sector analytics

✔ Agent trace visibility

✔ Conversational interface