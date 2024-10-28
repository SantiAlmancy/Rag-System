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

def process_text(text):
    # Process the input text through the defined steps.
    return processor.process(text)

def preprocess_text_column(df, text_column):
    # Apply preprocessing to the specified text column.
    if text_column in df.columns:
        df['processed_text'] = df[text_column].apply(process_text)
    else:
        print(f"Column '{text_column}' not found in DataFrame.")
