# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from builtins import print
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
import requests
import psycopg2
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

# ///METODOS

class ActionHelloWorld(Action):
	def name(self):
		return 'action_tiempo'

	def run(self, dispatcher, tracker, domain):

		location = tracker.get_slot('ciudad')

		params = {
  		'access_key': '94439daad766c32c4a44a4df64bac958',
  		'query': location
		}
		print(params)

		api_result = requests.get('http://api.weatherstack.com/current', params)

		api_response = api_result.json()

		print(api_response)

		country=api_response['location']['country']
		city=api_response['location']['name']
		condition=api_response['location']['localtime']
		temperature_c=api_response['current']['temperature']
		humidity=api_response['current']['humidity']
		wind_mph=api_response['current']['wind_speed']


		response ="""Actualmente son {} en {}. La temperatura es de {} grados, la humedad es de {} y la velocidad del viento de {} km""".format(condition, city, temperature_c, humidity, wind_mph)

		dispatcher.utter_message(response)

		return []


class ActionDatosAlumno(Action):
	def name(self):
		return 'action_datos_alumno'

	def run(self, dispatcher, tracker, domain):
		matricula = tracker.get_slot('matricula')
		print(matricula)
		conn = psycopg2.connect(host="localhost",database="alumno",user="postgres",password="admin")
		print(conn)
		cur = conn.cursor()
		cur.execute("select apellido, nombre from alumno as a where a.matricula like '{}'".format(matricula))
		row = cur.fetchone()
		# while row is not None:
		# 	print(row)
		# 	row=cur.fetchone()
		print(row)
		response="""El alummo con esa matricula es: {} """.format(row)
		dispatcher.utter_message(response)
		return []

class ActionMaterias(Action):
	def name(self):
		return 'action_materia'

	def run(self, dispatcher, tracker, domain):
		matricula = tracker.get_slot('matricula')
		print(matricula)
		conn = psycopg2.connect(host="localhost",database="alumno",user="postgres",password="admin")
		cur = conn.cursor()
		cur.execute("SELECT ma.nombre FROM materiacursada as m INNER join materia as ma ON m.materia_id = ma.id  INNER JOIN alumno as alu ON m.alumno_id = alu.id where alu.matricula like '{}'".format(matricula))
		row = cur.fetchone()
		dispatcher.utter_message("Las materias que curso ese alumno son:")
		while row is not None:
			print(row)
			dispatcher.utter_message("{}".format(row))
			row = cur.fetchone()
		return[]
