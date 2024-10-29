import requests
from bs4 import BeautifulSoup
import pandas as pd

# Read URLs from a .txt file
with open('urls.txt', 'r') as file:
    urls = file.read().splitlines()  # Read all lines and strip newline characters

# Initialize an empty DataFrame with Name and Text columns
df = pd.DataFrame(columns=["Name", "Text"])

# Iterate over each URL
for url in urls:
    print(url)
    # Send a request to the page
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the car name
    car_name = soup.find('span', class_='carheader').text.strip()

    # Extract the car text
    intelliTxt_span = soup.find('span', id='intelliTxt')
    if intelliTxt_span:
        text = intelliTxt_span.get_text(separator="\n", strip=True)
    else:
        text = None  # Handle case where text is not found

    # Create a new DataFrame for the current URL's data
    new_data = pd.DataFrame({"Name": [car_name], "Text": [text]})

    # Concatenate the new DataFrame with the existing one
    df = pd.concat([df, new_data], ignore_index=True)

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file
df.to_csv('carData.csv', index=False)