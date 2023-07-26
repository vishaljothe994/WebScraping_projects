import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lists to store the extracted data
Product_name = []
Prices = []
Description = []
Reviews = []

try:
    # Loop through pages 2 to 11
    for i in range(2, 12):
        url = 'https://www.flipkart.com/search?q=mobile+under+15000+rs&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_4_13_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_4_13_na_na_na&as-pos=4&as-type=RECENT&suggestionId=mobile+under+15000+rs&requestId=39ad8166-c429-4f7d-9583-225f094014fc&as-backfill=on&page='+str(i)

        # Fetch the web page
        source = requests.get(url)
        source.raise_for_status()  # Raise an exception for any HTTP errors
        soup = BeautifulSoup(source.text, 'lxml')

        # Find the box containing the product details
        box = soup.find("div", class_="_1YokD2 _3Mn1Gg")

        # Extract product names
        names = soup.find_all("div", class_="_4rR01T")
        for name in names:
            Product_name.append(name.text)
        print(len(Product_name))   


        # Extract product prices
        prices = box.find_all("div", class_="_30jeq3 _1_WHN1")
        for price in prices:
            try:
                # If the price is available, append it to the Prices list
                Prices.append(price.text)
            except AttributeError:
                # If the price is not available, append "Price: Not Available"
                Prices.append(0)
        print(len(Prices))   


        # Extract product descriptions
        desc = box.find_all("ul", class_="_1xgFaf")
        for description in desc:
            Description.append(description.text)

        print(len(Description))

        # # Extract product reviews
        # reviews = box.find_all("div", class_="_3LWZlK")
        # for review in reviews:
        #     Reviews.append(review.text)
        # print(len(Reviews))   


except requests.exceptions.RequestException as e:
    # Handle exceptions related to web requests
    print("Error occurred during web request:", e)

except Exception as e:
    # Handle other unexpected exceptions
    print("An unexpected error occurred:", e)

# Create a pandas DataFrame with the collected data
# df = pd.DataFrame({"Product Name": Product_name, "Prices": Prices, "Description": Description, "Reviews": Reviews})
df = pd.DataFrame({"Product Name": Product_name, "Prices": Prices, "Description": Description})


# Save the DataFrame to a CSV file
try:
    df.to_csv("flipkart_mobile_under_15000.csv", index=False)
    print("Data has been successfully saved to 'flipkart_mobile_under_15000.csv'.")
except Exception as e:
    print("An error occurred while saving the data:", e)