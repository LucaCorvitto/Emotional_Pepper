from pepper_functions import *

class FirstApproach:

    def __init__(self):
        self.sensor = Sensor()
        self.dialogue = Dialogue()
        self.full_memory = Memory('users_data.json')
        self.user_memory = Memory('current_user.json')
        self.emotion = Emotion()
        try:
            self.users_data = self.full_memory.load_data() # keep trace of every user Pepper interacted with
        except:
            self.users_data = {}
        self.start_int = 'no'
        self.start_quiz = 'no'
        self.user_classification = None

    def interact(self):
        
        personApp = self.sensor.sense(False, 1.0, 0.0, 3.0)

        if personApp:
            # keep starting interaction
            self.dialogue.say("What's your name?")
            user_name = self.dialogue.listen()

            # check if user is known
            if user_name not in self.users_data:
                self.dialogue.say("Nice to meet you {}. My name is Pepper. How old are you?".format(user_name))
                user_age = int(self.dialogue.listen(what_requires = 'age'))
                # wrong answers are checked in dialogue
                self.users_data[user_name] = {}
                self.users_data[user_name]['user_age'] = user_age #collects user age inside the user_name key
                self.user_classification = None
                self.users_data[user_name]['user_classification'] = self.user_classification
                self.users_data[user_name]['user_score'] = None
            else:
                self.dialogue.say("Nice to see you again, {}!".format(user_name))
                user_age = self.users_data[user_name]['user_age']
                # check if user already did the quiz
                if self.users_data[user_name]['user_score']:
                    self.user_classification = self.users_data[user_name]['user_classification']
                    user_score = self.users_data[user_name]['user_score']
                    # ask to the user if he wants to try again with the quiz
                    if user_score == 'happy':
                        self.dialogue.say("Last time you did really well with the quiz! Do you want to play again anyway?")
                        self.start_quiz = self.dialogue.listen(what_requires = 'answer')
                        if self.start_quiz != 'yes':
                            self.emotion.sad_emotional_response(mode='person_approaching')
                            self.dialogue.say("Nevermind, you can try again whenever you want! Until next time!")
                            return self.interact()
                        else:
                            self.emotion.happy_emotional_response(mode='person_approaching')
                            self.dialogue.say("Let's not waste time then, let's play again!")
                    else:
                        self.dialogue.say("Last time you didn't remember much... Do you want to try again the quiz?")
                        self.start_quiz = self.dialogue.listen(what_requires = 'answer')
                        if self.start_quiz != 'yes':
                            self.emotion.sad_emotional_response(mode='person_approaching')
                            self.dialogue.say("Nevermind, bye.")
                            return self.interact()
                        else:
                            self.emotion.happy_emotional_response(mode='person_approaching')
                            self.dialogue.say("Perfect, let's see what you can do this time.")


            if self.start_quiz != 'yes':
                # ask the user what they want to do
                print('entering permission loop')
                while(self.start_int != 'yes'):            

                    self.dialogue.say("I want to get to know each other better, can I ask you some questions?")
                    self.start_int = self.dialogue.listen(what_requires = 'answer')

                    print(self.start_int)
                    # if the user do not want to take the interview
                    if self.start_int != 'yes':
                        self.emotion.sad_emotional_response(mode='person_approaching')
                        self.dialogue.say("Uh, okay. Let me know if and when you are prepared to talk with me! I will wait for you!")
                        time.sleep(3.0)
                        return self.interact() #repeat the interaction from the start
                    
            
            # user accepted to go on
            next_is_interview = True if self.start_int == 'yes' else False
            current_user = {'user_name': user_name, 'user_age': user_age, 'user_classification': self.user_classification}
            self.user_memory.save_data(current_user)
            self.full_memory.save_data(self.users_data)
            return current_user, next_is_interview

