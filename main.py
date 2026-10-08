from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

header = {
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",
}

URL = "https://appbrewery.github.io/instant_pot/"

response = requests.get(url=URL, headers=header).text
soup = BeautifulSoup(response, "html.parser")

price = soup.find(class_="a-offscreen").get_text()
price_without_currency = float(price.split("$")[1])

smtp = os.getenv("SMTP_ADDRESS")
email = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")

MY_PRICE = float(105)

if price_without_currency < MY_PRICE:
    with smtplib.SMTP(smtp, port=587) as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=email, to_addrs="brainstrom.alex@gmail.com", msg=f"Subject:Price Down\n\n"
                                                                                   f"Instant Pot Duo Plus 9-in-1 Electric Pressure Cooker,"
                                                                                       f" Slow Cooker, Rice Cooker, Steamer,"
                                                                                       f" Saute, Yogurt Maker, Warmer & Sterilizer,"
                                                                                       f" Includes App With Over 800 Recipes,"
                                                                                       f" Stainless Steel, 3 Quart is now ${price_without_currency}")