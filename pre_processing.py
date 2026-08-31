import pandas as pd
import numpy as np
import re
import emoji

# Cleaning Text Function

def clean_text(text):
    text = re.sub(r'@\w+', '[USER]', text)
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"\brt\b", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r'[\n\r\t]+', ' ', text)
    text = re.sub(r"(\w+)\^2", r"\1 \1", text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[\u1160\u3164]', '', text)

    return text.strip()

# Remove Emoji Function
def remove_emoji(text):
    return emoji.replace_emoji(text, replace='') 

def smart_case(text):
    words = text.split()
    result = []
    for word in words:
        if word == 'USER' or word == '[URL]':
            result.append(word)

        elif len(word) >= 2 and word.isupper():
            result.append(word)
        # Lowercase hanya untuk huruf awal kalimat)
        else:
            result.append(word.lower())
    return ' '.join(result)

def preprocess(text):

    text = clean_text(text)
    text = remove_emoji(text)
    text = smart_case(text)

    return text