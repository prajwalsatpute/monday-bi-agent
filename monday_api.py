import requests
from config import MONDAY_API_TOKEN, MONDAY_API_URL


headers = {
    "Authorization": MONDAY_API_TOKEN,
    "Content-Type": "application/json",
}


def fetch_board_items(board_name):
    query = """
    query {
      boards {
        id
        name
        items_page(limit: 500) {
          items {
            name
            column_values {
                column {
                    title
                }
                text
                value
            }
          }
        }
      }
    }
    """

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query},
        headers=headers,
    )

    data = response.json()
    print("MONDAY API RESPONSE:", data)

    # --- DEBUG SAFE CHECK ---
    if "data" not in data:
        print("MONDAY API ERROR:", data)
        return []

    boards = data["data"]["boards"]

    for b in boards:
        if b["name"] == board_name:
            return b["items_page"]["items"]

    return []