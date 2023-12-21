import os, sys
import time
import json
import numpy as np
import wave, contextlib

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *

class Memory():

	def __init__(self, json_file):
		self.json_file = json_file

	def save_data(self, user_info):
		with open(self.json_file, 'w') as f:
			json.dump(user_info,f)
		return user_info

	def load_data(self):
		with open(self.json_file, 'r') as f:
			people_info = json.load(f)
		return people_info
	
	def update_data(self,name,score,calssification):
		users_info = self.load_data()
		users_info[name]['user_score'] = score
		users_info[name]['user_classification'] = calssification
		self.save_data(users_info)

class Initialization():

	def __init__(self, alive = True, speed = 80):
		pepper_cmd.robot.setAlive(alive)
		# if setAlive does not work try to setting it Alive manually:
		self.bm_service = pepper_cmd.robot.session_service("ALBackgroundMovement")
		self.ba_service = pepper_cmd.robot.session_service("ALBasicAwareness")
		self.sm_service = pepper_cmd.robot.session_service("ALSpeakingMovement")

		#setAlive
		self.bm_service.setEnabled(True)
		self.ba_service.setEnabled(True)
		self.sm_service.setEnabled(True)

		pepper_cmd.robot.tts_service.setParameter("speed", speed)

class Dialogue():

	def __init__(self, speed = 50):
		Initialization(speed = speed)
		self.default_vocab = ['luca', 'lorenzo', 'iocchi', 'patrizi']
		self.ans_vocab = ['yes', 'no', 'maybe']
		self.age_vocab = [str(i) for i in range(150)]
		self.repetition = 0

	def say(self, sentence, answer_time_window = 0, sleeping_time = 0.0):
		pepper_cmd.robot.say(sentence)

		if answer_time_window:
			return self.listen(timeout = answer_time_window)
		
		if sleeping_time:
			time.sleep(sleeping_time)

	def listen(self, timeout = 30, what_requires = 'aything'): # it can requires: answer, age
		
		if what_requires == 'answer': #interview 
			answer = pepper_cmd.robot.asr(vocabulary = self.ans_vocab, timeout = timeout)

			while answer not in self.ans_vocab:
				if not answer:
					answer = self.say(sentence = "Sorry, I did not hear you, repeat please.", answer_time_window = 30)
				else:
					answer = self.say(sentence= "Sorry for my lack of comprehension, but I need you to answer with just 'yes', 'no' or 'maybe'.", answer_time_window = 30)
		
		elif what_requires == 'age': #requesting age
			answer = pepper_cmd.robot.asr(vocabulary = self.age_vocab, timeout = timeout)

			while answer not in self.age_vocab:
				if not answer:
					answer = self.say(sentence = "Sorry, I did not hear you, repeat please.", answer_time_window = 30)
				else:
					# check if user's age is an integer
					try:
						if int(answer):
							in_answer = self.say(sentence = "Are you sure {} is your age? Please answer with just yes or no.".format(answer), answer_time_window = 30)
							if in_answer == 'yes':
								self.say(sentence='Uh, okay then.')
								return answer
							else:
								answer = self.say(sentence= 'So, what is really your age?', answer_time_window = 30)
					except:
						answer = self.say(sentence= 'Sorry, but I need you to answer me with an integer number.', answer_time_window = 30)
					
		
		else: # requesting name and other cases
			answer = pepper_cmd.robot.asr(vocabulary= self.default_vocab, timeout = timeout)

			while not answer:
				answer = self.say(sentence = "Sorry, I did not hear you, repeat please.", answer_time_window = 30)

		return answer

class Sensor():
	def __init__(self):
		Initialization(speed=200)
		self.dialogue = Dialogue()
		self.count = 0
	
	def sense(self, approaching = False, T = 1.0, start_time=0.0, wait_time=4.0):
		pepper_cmd.robot.startSensorMonitor() #start sensing
		if not approaching:
			print("Waiting for signal...")
			try:
				while not approaching:
					sensed = pepper_cmd.robot.sensorvalue() #value sensed
					approaching = (0.0 < sensed[1] < T) or (0.0 < sensed[2] < T)
					start_time = time.time()
			except KeyboardInterrupt:
				pepper_cmd.robot.stopSensorMonitor()
				sys.exit(0)
			return self.sense(True, 1.0, start_time, 4.0)
		else:
			print("Person approaching...")
			while approaching:
				sensed = pepper_cmd.robot.sensorvalue()
				front = (0.0 < sensed[1] < T)
				back = (0.0 < sensed[2] < T)
				approaching = front or back
				if time.time() - start_time >= wait_time:					
					if back:
                        # wait for person to leave
						print("Person waiting back")
						while(back):
							if self.count == 0:
								self.dialogue.say("Please come in front of me, I feel a bit uneasy if you stay behind me while we talk.")
								self.count+=1
							else:
								self.dialogue.say("Please come in front of me.")
							time.sleep(5.0)
							sensed = pepper_cmd.robot.sensorvalue()
							back = (0.0 < sensed[2] < T)
					if front:
						print("Person waiting to approach")
						if self.count == 0:
							self.dialogue.say("Hello!")
						else:
							self.dialogue.say("Hello! Thank you for accepting my request!")
							self.count=0
						pepper_cmd.robot.stopSensorMonitor() #stop sensing
						return True
				else:
					front = False
					back = False
			if not front:
				print("They was just passing by.")
				return self.sense(False, 1.0, 0.0, 4.0)

class Move():
	
	def __init__(self, speed = 200):
		Initialization(speed = speed)
		# HY  -  HeadYaw,			HP -  HeadPitch,			LSP -  LShoulderPitch,
		# LSR -  LShoulderRoll,	    LEY -  LElbowYaw,			LER -  LElbowRoll, 
		# LWY -  LWristYaw,		    RSP -  RShoulderPitch,	    RSR -  RShoulderRoll, 
		# REY -  RElbowYaw,		    RER - RElbowRoll,		    RWY - RWristYaw
		# LH - LHand,			    RH - RHand,				    HipR - HipRoll,
		# HipP - HipPitch,		    KP - KneePitch

		self.jointNames = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
               "LHand", "RHand", "HipRoll", "HipPitch", "KneePitch"]

		self.InputJoints = {"HY":0, "HP":1, "LSP":2, "LSR":3, "LEY":4,"LER":5, "LWY":6, "RSP":7, 
			"RSR":8, "REY":9, "RER":10,"RWY":11, "LH":12, "RH":13, "HipR":14, "HipP":15, "KP":16}

	def change_posture(self, joints, values, sleeping_time = 0.5, stiff=False):
		joint_list = []
		joint_values = []
		posture = pepper_cmd.robot.getPosture()

		for i, (j, v) in enumerate(zip(joints, values)):
			# input v is in degrees so I will turn into radians
			joint_values.append(v*np.pi/180)
			joint_list.append(self.jointNames[self.InputJoints[j]])

		pepper_cmd.robot.motion_service.angleInterpolation(joint_list,joint_values,1.0,True)
		if stiff:
			end_time = time.time() + sleeping_time
			while time.time() < end_time:
				pepper_cmd.robot.motion_service.angleInterpolation(joint_list,joint_values,1.0,True)
		else:
			time.sleep(sleeping_time)
		print("Posture changed in joints: {}".format(joint_list))

		return posture

class Emotion():

	def __init__(self, speed = 50):
		Initialization(speed = speed)
		self.dialogue = Dialogue()
		self.rp_service = pepper_cmd.robot.session_service("ALRobotPosture")
		self.move = Move()

	def reaction(self, user_response, mode="interview"):
		print(user_response)

		if user_response >= 1:
			print("Positive emotive reaction")
			if mode == "interview":
				self.dialogue.say("Yeee!")
			elif mode == 'quiz':
				self.dialogue.say("Wow! You did remember a lot about me, thanks!")
			self.move.change_posture(["LWY","RWY","LSP","RSP"],[-90,90,40,40],sleeping_time=0.1)
			self.move.change_posture(["LWY","RWY","LSP","RSP","LER","RER"],[-90,90,90,90,-90,90],sleeping_time=0.5)
			# come back to initial position
			self.rp_service.goToPosture('Stand',1.0)
		elif user_response == 0:
			print("Neutral emotive reaction")
			self.dialogue.say("Understood.")
			time.sleep(1)
			self.rp_service.goToPosture('Stand',1.0)
		else:
			print("Negative emotive reaction")
			if mode == "interview":
				self.dialogue.say("Oh.")
			elif mode == 'quiz':
				self.dialogue.say("Oh, you didn't pay attention when I was speaking, did you?")
			end_time = time.time() + 1
			while time.time() < end_time:
				self.rp_service.goToPosture('Crouch',1.0)
			#time.sleep(1.0)
			self.rp_service.goToPosture('Stand',1.0)

		if mode == "quiz":
			if user_response >=0:
				self.dialogue.say("Thank you for your time, I hope you enjoyed the time spent together as much as I did! Until next time!")
				self.move.change_posture(["LWY","RWY","LSP","RSP"],[-90,90,40,40],sleeping_time=0.1)
				self.move.change_posture(["LWY","RWY","LSP","RSP","LER","RER"],[-90,90,90,90,-90,90],sleeping_time=0.5)
				self.rp_service.goToPosture('Stand',1.0)
			else:
				self.dialogue.say("Thank you for your time, bye.")
				end_time = time.time() + 1
				while time.time() < end_time:
					self.rp_service.goToPosture('Crouch',1.0)
				self.rp_service.goToPosture('Stand',1.0)
		
		return
	
	def happy_emotional_response(self, mode):
		self.reaction(1,mode=mode)
		return
	
	def sad_emotional_response(self,mode):
		self.reaction(-1,mode=mode)
		return
	

# class Music():

# 	def __init__(self, music_path = ''):
# 		self.dialogue = Dialogue()
# 		self.music_path = music_path
# 		self.get_duration()
# 		self.rp_service = pepper_cmd.robot.session_service("ALRobotPosture")
# 		self.ap_service = pepper_cmd.robot.session.service("ALAudioPlayer")
# 		self.move = Move()

# 	def get_duration(self):
# 		with contextlib.closing(wave.open(self.music_path, 'r')) as f:
# 			frames = f.getnframes()
# 			rate = f.getframerate()
# 			self.duration = int(frames / float(rate)) - 4

# 	def play(self):
# 		self.dialogue.say("Alright! Let's listen to some relaxing music together.")
# 		self.ap_service.playFile(self.music_path, _async = True)
# 		#ap_service.playFile('/home/nao/audio/whatever it takes.wav', _async = True)
# 		curr_time = time.time()
		
# 		#take posture of flute players
# 		self.move.change_posture(["LWY","RWY","LER","RER","LSP","RSP","LSR","RSR"],[45,90,-90,90,10,10,90,90], sleeping_time=0.5, stiff=True)

# 		while time.time() - curr_time < self.duration: #loop of the same movements
# 			self.move.change_posture(["LWY","RWY","LER","RER","LSP","RSP","LSR","RSR","HipR"],[45,90,-90,90,10,10,90,90,20], sleeping_time=1, stiff=True)
# 			self.move.change_posture(["LWY","RWY","LER","RER","LSP","RSP","LSR","RSR","HipR"],[45,90,-90,90,10,10,90,90,-20], sleeping_time=1, stiff=True)
# 			# self.move.change_posture(["HipR"],[20],sleeping_time=1.0)
# 			# self.move.change_posture(["HipR"],[-20],sleeping_time=1.0)

# 		self.rp_service.goToPosture('Stand',1.0)
		
# 		pepper_cmd.robot.normalPosture()
# 		self.dialogue.say("Did you enjoy it? Now it is QUIZ TIME!")