from interview import *

hard_threshold = 5
medium_threshold = 1
### save the score

def execute_action(action, interview):
    action = action.split()[0]
    print('executing action: ', action)

    if action == "INTERVIEW_USER":
        interview.ask_questions()
        print('### Interview ended ###')
        return 
    elif action == "CHECK_USER_INTERVIEW_HARD":
        if interview.user_level >= hard_threshold:
            return True
    elif action == "CHECK_USER_INTERVIEW_MEDIUM":
        if interview.user_level >= hard_threshold:
            return True
    elif action == "CLASSIFY_HARD_TRUE":
        return 'hard'
    elif action == "CLASSIFY_HARD_FALSE":
        return False
    elif action == "CLASSIFY_MEDIUM_TRUE":
        return 'medium'
    elif action == "CLASSIFY_MEDIUM_FALSE":
        return False
    elif action == "CLASSIFY_EASY_TRUE":
        return 'easy'

def run_interview(interview):
    plan = 'plans/interview.txt'

    with open(plan) as f:
        lines = f.readlines()
        next_action = "0||0"

        for line in lines:

            if next_action in line:

                try:
                    id, action, trueson, falseson = line.strip('\n').strip(' ').split(' --- ')
                    true_id = trueson.split(': ')[1]
                    false_id = falseson.split(': ')[1]

                    print("id: ", id, "action: ", action)
                    print("trueson: ", trueson, "falseson: ", falseson)

                    res = execute_action(action, interview)

                    if type(res) == str:
                        return res

                    if res:
                        next_action = true_id
                    else:
                        next_action = false_id

                except: 
                    id, action, son = line.strip('\n').strip(' ').split(' --- ')
                    son_id = son.split(': ')[1]

                    print("id: ", id, "action: ", action, "son: ", son)

                    res = execute_action(action, interview)

                    if type(res) == str:
                        return res

                    next_action = son_id #there is always a known action since there is only one son