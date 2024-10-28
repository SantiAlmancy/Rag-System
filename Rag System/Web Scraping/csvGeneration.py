import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = "https://www.ultimatecarpage.com/car/8101/Williams-FW43B-Mercedes.html"

# Send a request to the page
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize an empty DataFrame
df = pd.DataFrame()

# Extract the car name
carName = soup.find('span', class_='carheader').text.strip()

# Add the car name as a column in the DataFrame
df["Name"] = [carName]

# Add the car text as a column in the DataFrame
intelliTxt_span = soup.find('span', id='intelliTxt')
if intelliTxt_span:
    text = intelliTxt_span.get_text(separator="\n", strip=True)
    df["Text"] = [text] 

# Display the DataFrame
print(df)