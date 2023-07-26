import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.imdb.com/list/ls068082370/'

try :
    source = requests.get(url)
    source.raise_for_status()

    # print(source)

    soup = BeautifulSoup(source.text, 'html.parser')
    # print(soup)

    movie_data = []

    movie_items = soup.find_all('div', class_='lister-item mode-detail')

    # print(len(movie_items))

    for item in movie_items:
        header = item.find('h3', class_='lister-item-header')
        title = header.a.text.strip()
        year = header.find('span', class_='lister-item-year').text.strip()
        rating = item.find('span', class_='ipl-rating-star__rating').text.strip()
        num = item.find('span', class_='lister-item-index unbold text-primary').text.strip(".")
        print(f"Number: {num}, Title: {title}, Rating: {rating}, Year: {year}")

        movie_data.append({
            'Number': num,
            'Title': title,
            'Rating': rating,
            'Year': year
        })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(movie_data)

    # Save the DataFrame to an Excel file
    output_file = 'imdb_movie_list.xlsx'
    df.to_excel(output_file, index=False)

    print(f"Data has been saved to '{output_file}' successfully.")    



except Exception as e:
    print(e)