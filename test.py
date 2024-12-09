def get_csrf_token(session):

    import re

    url = "https://www.roblox.com/catalog/"

    response = session.get(url)
    response.raise_for_status()

    token_pattern = "setToken\\('(?P<csrf_token>[^\\)]+)'\\)"

    match = re.search(token_pattern, response.text)
    assert match
    return match.group("csrf_token")

def get_assets(session, params):

    url = "https://catalog.roblox.com/v1/search/items"

    response = session.get(url, params=params, headers={})
    response.raise_for_status()

    return {"items": [{**d, "key": f"{d['itemType']}_{d['id']}"} for d in response.json()["data"]]}

def get_items(session, csrf_token, assets):

    import json

    url = "https://catalog.roblox.com/v1/catalog/items/details"

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "X-CSRF-TOKEN": csrf_token
    }

    response = session.post(url, data=json.dumps(assets), headers=headers)
    response.raise_for_status()

    items = response.json()["data"]
    return items

def main():

    import requests

    session = requests.Session()

    params = {
        "category": "Collectibles",
        "limit": "60",
        "sortType": "4",
        "subcategory": "Collectibles"
    }

    csrf_token = get_csrf_token(session)
    assets = get_assets(session, params)
    items = get_items(session, csrf_token, assets)

    first_item = items[0]

    for key, value in first_item.items():
        print(f"{key}: {value}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())