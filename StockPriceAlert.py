import requests
from twilio.rest import Client
import os

STOCK_NAME = "NVDA"
COMPANY_NAME = "NVIDIA"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

# 1. - Get yesterday's closing stock price.

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]  # list and dictionary comprehension
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

print(yesterday_closing_price)

# 2. - Get the day before yesterday's closing stock price

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

print(day_before_yesterday_closing_price)

# 3. - Find the absolute difference between 1 and 2

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "📈"
else:
    up_down = "🔻"

print(difference)

# 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

# 5. - If diff_percentage is greater than 5 then fetch 3 news pieces from the news endpoint.
# 6. - Use the News API to get articles related to the COMPANY_NAME.

if abs(diff_percent) > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

# 7. - Use Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]
    print(three_articles)

# 8. - Create a new list of the first 3 article's headline and description using list comprehension.

    # [new_item for item in list]
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

# 9. - Send each article as a separate message via Twilio.

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
                             body=article,
                             from_="enter Twilio phone number",
                             to="enter recipient's number"
                         )

