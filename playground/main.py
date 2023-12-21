from interview import *
from interview_planner import *
from person_approaching import *
#from app_runner import app_run
from tablet.app import start_server
# from Emotive_response import *
# from pepper_functions import Music

import subprocess
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-ap','--approach', action='store_true')
    parser.add_argument('-in', '--interview', action='store_true')
    parser.add_argument('-qz', '--quiz', action='store_true')
    parser.add_argument('--diff', type=str, default='easy')
    #parser.add_argument('-mu', '--music', action='store_true')

    args = parser.parse_args()
    approach = args.approach
    inter = args.interview
    quiz = args.quiz
    diff = args.diff
    #music = args.music

    full_memory = Memory('users_data.json')
    user_memory = Memory('current_user.json')

    #default case: run the entire interaction
    if not approach and not inter and not quiz:# and not music:
        approach = True
        inter = True
        quiz = True

    if not approach:
        interaction_info = {'user_name':'Mario', 'user_age': 18, 'user_classification':diff}
        next_is_interview = True

    begin()

    # check person_approaching
    if approach:
        first_approach = FirstApproach()
        interaction_info, next_is_interview = first_approach.interact()


    # start interview
    if inter:
        if next_is_interview:
            interview = Interview(interaction_info)
            #interview.ask_questions()
            user_classification = run_interview(interview) #executes a pddl plan
            print("The user was classified as: ", user_classification)
            #save user_classification
            interaction_info['user_classification'] = user_classification
    user_memory.save_data(interaction_info)

    # # play music
    # if music:
    #     play = Music('music/Off-Seer-Crys_XC3.wav')
    #     play.play()

    #start tablet interaction;
    if quiz:
        #subprocess.run(["python", "app.py"])
        start_server()
        #app_run() # start tablet interaction
        #print('quiz')

    end()

    return

if __name__=="__main__":
    main()