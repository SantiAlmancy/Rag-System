import os
import pandas as pd
from dataCleaning import *
from dataPreparation import *
from dotenv import load_dotenv 

class TextProcessor:
    def __init__(self):
        self.steps = []

    def add_step(self, function):
        self.steps.append(function)

    def process(self, text):
        for step in self.steps:
            text = step(text)
        return text

# Special Characters Removal
specialCharactersToRemove = [
    '~', '`', '@', '#', '$', '%', '^', '&', '*', '(', ')',
    '_', '+', '=', '{', '}', '[', ']', '|', ':', ';', '"',
    "'", '<', '>', ',', '.', '/', '-', '\n', '\t', '\r', '\x0b', '\x0c'
]

# Create a text processor
processor = TextProcessor()

# Steps to the pipeline
processor.add_step(stopWordsRemoval)
processor.add_step(lemmatizer)
processor.add_step(singleCharactersRemoval)
processor.add_step(htmlTagsRemoval)
processor.add_step(lambda text: specialCharactersRemoval(text, specialCharactersToRemove))
processor.add_step(multipleSpacesRemoval)

def processText(text):
    # Process the input text through the defined steps.
    return processor.process(text)

def preprocessColumns(df, columns):
    for column in columns:
        if column in df.columns:
            df[column] = df[column].apply(processText)
    return df

def main():
    # Load the CSV file
    load_dotenv() 
    DATA_PATH = os.getenv("DATA_PATH")
    df = pd.read_csv(DATA_PATH)
    
    # Specify the text column to preprocess
    columnsToPreprocess  = ['Name', 'Text']
    preprocessColumns(df, columnsToPreprocess )
    
    # Display the full text of the first three entries in the "text" column
    for i, text in enumerate(df['Text'].head(3), start=1):
        print(f"Text entry {i}:\n{text}\n{'-'*40}\n")

    # Save the processed DataFrame to a new CSV file
    PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH")
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Processed data saved to {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    main()
