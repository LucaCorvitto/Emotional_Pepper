import sys
#from interview import *

#the planner checks the next action to execute
def next_action(quiz_difficulty, last_action, last_result=True):
    print("### Last executed action: {} ###".format(last_action))

    if quiz_difficulty == 'easy':
        plan = 'plans/quiz_easy.txt'
    elif quiz_difficulty == 'medium':
        plan = 'plans/quiz_medium.txt'
    else:
        plan = 'plans/quiz_hard.txt'

    next_action_found = False
    next_action = last_action

    with open(plan) as f:
        lines = f.readlines()

        for line in lines:

            if next_action in line:

                try: # se ha due figli
                    id, action, trueson, falseson = line.strip('\n').strip(' ').split(' --- ')
                    true_id = trueson.split(': ')[1]
                    false_id = falseson.split(': ')[1]

                    print("id: ", id, "action: ", action)
                    print("trueson: ", trueson, "falseson: ", falseson)

                    #if next action is found then return it, else find it
                    if next_action_found:
                        return action, id

                    if id != last_action:
                        continue
                    else:
                        next_action_found = True

                    if last_result: # se la risposta e' corretta
                        next_action = true_id
                    else: #risposta errata
                        next_action = false_id

                except: # se ha un figlio
                    id, action, son = line.strip('\n').strip(' ').split(' --- ')
                    son_id = son.split(': ')[1]
                    print("id: ", id, "action: ", action, "son: ", son)

                    #if next action is found then return it, else find it
                    if next_action_found:
                        return action, id

                    if id != last_action:
                        continue
                    else:
                        next_action_found = True

                    next_action = son_id #there is always a known action since theere is only one son
