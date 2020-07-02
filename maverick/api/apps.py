from django.apps import AppConfig
import pandas
import json

from .mid import mediatorCall

class ApiConfig(AppConfig):
    name = 'api'

class Moderator(AppConfig):
	name = 'moderator'

	def moderator(msg):
		if (msg == "get_test"):
			return 'Testing vala'
		elif (msg == "input.welcome"):
			return 'Hello ji, django here'
		try:
			qa=mediatorCall(msg)
			output=qa.run_query()
			return output
		except:
			return msg
			# return {'msg':"I don't know what to make of it. Please refer to ReadMe.", 'data': None}
