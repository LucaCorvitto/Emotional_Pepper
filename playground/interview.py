import os
import sys
import time
from turtle import fd
from pepper_functions import *

DEBUGGING = False

answer1 = 'yes'
answer2 = 'no'
answer3 = 'maybe'

#per il momento non usati, quindi li commento
#from numpy.random import choice
#import csv
#import wave, contextlib
#import math

class Interview:
	def __init__(self, interaction_info):
		self.dialogue = Dialogue()
		#self.move = Move()
		self.emotion = Emotion()
		#self.vocabulary = [[answer1, answer2, answer3]]
		self.questions = ['Are you intimidated by robots?', 
					'Do you prefer humanoid robots over non-human ones?', 
					['Would you like it if one of your relatives played with a robot?',
	  					'Would you like it if a robot kept your grandparent company?',
						'Would you like to play with a robot?'], #question 02 
					'Are you excited about future advancements in robotics?',
					'Do you trust robots to do important activities like driving?',
					'Are you scared about the ethical implications of robot usage?',
					'Do you see robots as a threat to human society?']
		self.facts = ['',
				"I want to tell you more about me: I am from Japan.	Japan is the largest manufacturer of robots in the world with more than fifty percent of the world's robot manufactured in Japan.",
				"In Japan we have a lot of robots working in hotels as staff. Also, some factories are run entirely by robots, and they make other robots. Moreover, kids are taught about how to make a robotic arm in Holiday programs.",
				"Individual robots like me are now out of style. Researchers are studying swarm robotics, where large groups of simple robots work together in a coordinated way. This concept is inspired by the behavior of social insects like ants and bees.",
				'''Fukuoka SoftBank Hawks, which is a Japanese professional baseball team, has temporarily hired me and my Pepper friends. The largest robot cheerleading squad comprises 100 Pepper humanoid robots. The cheering squad won a Guinness World Record title, it is featured in 2022 edition.
				I won a Guinness world title!!! ''',
				"Do you know? Robots have been used extensively in space exploration. The Mars rovers, such as Spirit, Opportunity, and Curiosity, are examples of robots that have been exploring the Martian surface.",
				'']
		#self.user_info = load_data('current_user.json') #defined on ask_questions
		self.user_info = interaction_info
		self.user_answers = []
		#point values of every answer, +1 means the user likes robots, -1 he doesn't, 0 has no opinion
		self.answer_points = [[-1, 1, 0], [1, -1, 0], [1, -1, 0], [1, -1, 0], [1, -1, 0], [-1, 1, 0], [-1, 1, 0]]
		self.user_level = 0

	def ask_questions(self):
		self.dialogue.say("""Perfect! I will now make you different questions about what you think about robots and I need you to answer them with just "yes", "no" or "maybe". Are you ready? Let's begin!""")
		#asking all the questions to the user
		for i, question in enumerate(self.questions):
			if DEBUGGING and i == 3:
				break

			if i==2: # different question basing on the user's age
				if self.user_info['user_age'] >= 40:
					question = question[0]
				elif self.user_info['user_age'] >= 18:
					question = question[1]
				else: question = question[2]

			self.dialogue.say(question)
			user_answer = self.dialogue.listen(what_requires = 'answer').lower()
			self.user_answers.append(user_answer)
			#pepper acts with emotions
			self.emotional_reaction(i, user_answer)
			fact = self.facts[i]
			if fact != '':
				self.dialogue.say(fact)

		self.compute_user_level()
		print("user scored {} points in the interview".format(self.user_level))
		self.dialogue.say('Thank you for your patience! Now I will propose a simple quiz for you to solve on my tablet. Touch the screen to choose an answer.')

	def compute_user_level(self):
		points = 0
		#checking the table for point values of answers
		for i, answer in enumerate(self.user_answers):
			if answer == answer1:
				points += self.answer_points[i][0]
			elif answer == answer2:
				points += self.answer_points[i][1]
			else:
				points += self.answer_points[i][0]
		self.user_level = points

	def emotional_reaction(self, answer_idx, answer):
		if answer == answer1:
			mood = self.answer_points[answer_idx][0]
		elif answer == answer2:
			mood = self.answer_points[answer_idx][1]
		else:
			mood = self.answer_points[answer_idx][2]

		self.emotion.reaction(mood)