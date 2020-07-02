import nltk
import string
import json
import requests
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from keras.models import load_model
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 

nltk.download('wordnet')
nltk.download('stopwords')

class news_fun:

	def preprocess(self, text):
	    final_text = []
	    stopword = set(stopwords.words('english'))

	    words = text.split()

	    for i in words:
	        if i not in stopword:
	            final_text.append(i)

	    lemmatizer = WordNetLemmatizer() 
	    final_text = list(map(lambda x: lemmatizer.lemmatize(x,'v'), final_text))

	    return ' '.join(final_text)


	 def news_intent(self,category):

	    if not category:
	    	model = tf.keras.models.load_model("model.h5",custom_objects={'KerasLayer':hub.KerasLayer})

	        response = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=d2f436851a964bac8a47fd50be902da6")
	        data=pd.DataFrame(json.loads(response.text)['articles'])[['title','description','url','content']]
	        data = data.dropna().reindex()
	        X= pd.DataFrame()
	        X= data.title + " " + data.description + " " + data.content
	        X=pd.DataFrame(X)
	        data.drop(['description','content'],axis=1, inplace=True)

	        for i in range(X.shape[0]):
	            X.iloc[i,0] = self.preprocess(X.iloc[i,0])
	            
	        X = tf.data.Dataset.from_tensor_slices((X.values))
	        preds = model.predict(X)
	        preds = np.argmax(preds, axis=1)
	        data['category'] = preds
	        d=["sport", "general", "us", "business", "health", "entertainment", "technology"]
	        data.category = data.category.apply(lambda x: d[x])

	        data= pd.DataFrame(data.groupby(['category']).first())
	        output = {'msg': None, 'data': data}
	        return output
	    else:
	        t= "https://newsapi.org/v2/top-headlines?country=" + category + "&apiKey=d2f436851a964bac8a47fd50be902da6"
	        response = requests.get(t)
	        data=pd.DataFrame(json.loads(response.text)['articles'])[['title','url']]
	        output = {'msg': None, 'data': data}
	        return output







