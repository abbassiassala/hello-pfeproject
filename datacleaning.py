import re
from tqdm import tqdm_notebook, tqdm
from nltk.corpus import stopwords
from tensorflow.keras import regularizers, initializers, optimizers, callbacks
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.utils.np_utils import to_categorical
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential
import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')

df = pd.read_csv("scraped_article2.csv")
x = df['article_title']
y = df['article_text']
z=x+" "+y

print(x)

print(y)


print(z[0])

print(z[1])




stop_words = set(stopwords.words('english'))
def clean_text(text, remove_stopwords = True):
    output=""
    text = str(text).replace(r'http[\w:/\.]+','')#supprimer les urls
    text = str(text).replace(r'[^\.\w\s]','')
    text = str(text).replace(r'\.\.+','.')#remplacer multiple espaces avec un seul
    text = str(text).replace(r'\.',' . ')
    text = str(text).replace(r'\s\s+',' ')
    text = str(text).replace("\n", "")#supprimer les sauts de ligne
    text = re.sub(r'[^\w\s]','',text).lower() #lower text

    return text

texts = []
for line in x:
    texts.append(clean_text(line))







