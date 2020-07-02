#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import dialogflow
from google.api_core.exceptions import InvalidArgument


# In[7]:


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
DIALOGFLOW_PROJECT_ID = 'api-test-hctppy'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'


# In[22]:


text_to_be_analyzed = 'Yes' 


# In[23]:


session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.types.QueryInput(text=text_input)
try:
    response = session_client.detect_intent(session=session, query_input=query_input)
except InvalidArgument:
    raise

print("Query text:", response.query_result.query_text)
print("Detected intent:", response.query_result.intent.display_name)
print("Detected intent confidence:", response.query_result.intent_detection_confidence)
print("Fulfillment text:", response.query_result.fulfillment_text)


# In[76]:


response


# In[ ]:




