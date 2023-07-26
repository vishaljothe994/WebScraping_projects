import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to perform web scraping on a given URL
def scrape_movie_data(url):
    try:
        source = requests.get(url)
        source.raise_for_status()
        soup = BeautifulSoup(source.text, 'html.parser')

        movie_data = []
        movie_items = soup.find_all('div', class_='lister-item mode-detail')

        for item in movie_items:
            # Extracting the movie title
            header = item.find('h3', class_='lister-item-header')
            title = header.a.text.strip()

            # Extracting the movie release year
            year = header.find('span', class_='lister-item-year').text.strip()

            # Extracting the movie rating
            rating = item.find('span', class_='ipl-rating-star__rating').text.strip()

            # Extracting the movie number
            num = item.find('span', class_='lister-item-index unbold text-primary').text.strip(".")
            print(f"Number: {num}, Title: {title}, Rating: {rating}, Year: {year}")

            # Appending the extracted data as a dictionary to the movie_data list
            movie_data.append({
                'Number': num,
                'Title': title,
                'Rating': rating,
                'Year': year
            })

        return movie_data

    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        return []


# URL of the IMDb list with multiple pages
url_template = 'https://www.imdb.com/list/ls068082370/?page={}'
all_movie_data = []
page = 1

# Loop through multiple pages and scrape data
while True:
    url = url_template.format(page)
    movie_data = scrape_movie_data(url)

    if not movie_data:
        # No more data to scrape, break out of the loop
        break

    all_movie_data.extend(movie_data)
    page += 1

# Create a DataFrame from the extracted data
df = pd.DataFrame(all_movie_data)

# Save the DataFrame to an Excel file
output_file = 'imdb_movie_list_pagination.xlsx'
df.to_excel(output_file, index=False)

print(f"Data has been saved to '{output_file}' successfully.")