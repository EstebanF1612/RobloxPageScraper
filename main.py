import joblib

def get_Games(data, params):
    for i in range(1, len(data['sorts'])):
        if (data['sorts'][i]['sortDisplayName'] == params):
            return [game for game in data['sorts'][i]['games'] if not game.get('isSponsored', False)]
    
    

def main():
    import requests
    
    print("Please input your device of inquiry (input \"all\" if research must be performed on all devices): ")
    device = input()
    if not device:
        device = "all"
    print("Please input your country of interest (input \"all\" if research must be performed on all countries): ")
    country = input()
    if not country:
        country = "all"

    # URL of the XHR request
    url = "https://apis.roblox.com/explore-api/v1/get-sorts"
    params = {
        "sessionId": "82002543-4da8-4c20-b66d-b323e7485a15", 
        "device": device,
        "country": country,
    }
    
    # Sending a GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        print("====================================\nData Obtained Successfully!\n====================================")
        print("From the following list:\n")
        for i in range(1, len(data['sorts'])):
            print(f"{i}. {data['sorts'][i]['sortDisplayName']}")
        
        print("\nPlease input the numbers of the categories you would like to analyze separated by commas: \n(tip: reducing the number of categories selected provides more accurate results)")
        categories = input()
        categories = categories.split(",")
        for i in range(len(categories)):
            categories[i] = int(categories[i])
        
        print("====================================\nData Segregation Complete!\n====================================")
        print("====================================\nBeggining Data Analysis\n====================================")
        
        for category in categories:
            categoryData = []
            match category:
                case [1]:
                    categoryData = get_Games(data, "Top Trending")
                case [2]:
                    categoryData = get_Games(data, "Up-and-Coming")
                case [3]:
                    categoryData = get_Games(data, "Fun with Friends")
                case [4]:
                    categoryData = get_Games(data, "Top Revisited")
                case [5]:
                    categoryData = get_Games(data, "Top Earning")
                    
            if (categoryData):
                print(f"Category {category} has {len(categoryData)} games")
            else:
                print(f"Category {category} is not valid\nSkipping...")
        print("====================================\nData Analysis Complete!\n====================================")
        
    else:
        print(f"Request failed with status code: {response.status_code}")

if __name__ == "__main__":
    import sys
    sys.exit(main())
    


# import requests
    
    # url = "https://www.roblox.com/charts"
    
    # session = requests.get(url)
    
    # # print(session.status_code)
    
    # print(session.text)
    # '''
    # params = {
        
    # }
    # '''
    
    # #csrf_token = get_csrf_token(session)