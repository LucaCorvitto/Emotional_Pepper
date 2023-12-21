import re
import sys
from flask import Flask, render_template, request, jsonify
#from views import views, render_template #import the views variable from the views file
#from flask import request, jsonify

sys.path.append('../')
from planner_for_server import *
from pepper_functions import *

total_score = 0
question_number = 1
name = None
difficulty = None
user_info = None
# user_info = load_data('current_user.json')
# difficulty = user_info['user_classification']
# name = user_info['user_name']
# default
#difficulty = "easy"
# name = "Zio Pera"

### things for pddl planner ###
last_action_id = "0||0"
current_action = ""
answers = {}

def update_actions(action, action_id):
    global last_action_id, current_action
    print("### Action_to_execute: ", action, "###")
    current_action = action
    last_action_id = action_id

def update_answers(current_action, answer):
    global answers
    question_name = current_action.split()[1]
    answers[question_name] = answer

def update_info():
    global user_info, difficulty, name
    user_info = Memory('current_user.json').load_data()
    difficulty = user_info['user_classification']
    name = user_info['user_name']
    
###############################

def start_evaluation(action):
    print('### Executing action: {} ###'.format(action))
    if 'HAPPY_EMOTIONAL_RESPONSE' in action:
        Emotion().happy_emotional_response(mode='quiz')
        # save the current user info updating the full_memory
        Memory('users_data.json').update_data(name,'happy',difficulty)
        return
    elif 'SAD_EMOTIONAL_RESPONSE' in action:
        Emotion().sad_emotional_response(mode='quiz')
        # save the current user info updating the full_memory
        Memory('users_data.json').update_data(name,'sad',difficulty)
        return
    elif 'CHECK_ANSWER' in action:
        question = action.split()[1]
        answer = answers[question]
        if answer == 'Correct answer':
            print("### Answer is TRUE ###")
            action, action_id = next_action(difficulty, last_action_id, True)
            update_actions(action, action_id)
            start_evaluation(action)
        elif answer == 'Wrong answer': 
            print("### Answer is FALSE ###")
            action, action_id = next_action(difficulty, last_action_id, False)
            update_actions(action, action_id)
            start_evaluation(action)
        else:
            print('ERROR')




app = Flask(__name__)   #application initialization
#app.register_blueprint(views, url_prefix="/views")

# Define a route for the root URL ("/")
@app.route("/")
def home():
    update_info()
    return render_template("quiz_start.html", name=user_info['user_name'])

@app.route("/quiz")
def next_question():
    #user_info = load_data('current_user.json')
    #difficulty = user_info['user_classification']
    if difficulty == "easy":
        if current_action == "SHOW_QUESTION QUESTION_GUINNESS":
            return render_template("/easy_guinnes.html")
        elif current_action == "SHOW_QUESTION QUESTION_MOON":
            return render_template("/easy_moon.html")
        elif current_action == "SHOW_QUESTION QUESTION_MADE":
            return render_template("/easy_made.html")
        elif current_action == "SHOW_QUESTION QUESTION_NAME":
            return render_template("/easy_name.html")
        else:
            print("quiz ended, the user answers were: ", answers)
            return render_template("/quiz_ended.html")
    if difficulty == "medium":
        if current_action == "SHOW_QUESTION QUESTION_MARS":
            return render_template("/medium_mars.html")
        elif current_action == "SHOW_QUESTION QUESTION_GUINNESS":
            return render_template("/medium_guinness.html")
        elif current_action == "SHOW_QUESTION QUESTION_SWARM":
            return render_template("/medium_swarm.html")
        elif current_action == "SHOW_QUESTION QUESTION_MANUFACTURED":
            return render_template("/medium_manufactured.html")
        else:
            print("Quiz ended, the user answers were: ", answers)
            return render_template("/quiz_ended.html")
    else:
        if current_action == "SHOW_QUESTION QUESTION_MARS":
            return render_template("/hard_mars.html")
        elif current_action == "SHOW_QUESTION QUESTION_BASEBALL":
            return render_template("/hard_baseball.html")
        elif current_action == "SHOW_QUESTION QUESTION_SWARM":
            return render_template("/hard_swarm.html")
        elif current_action == "SHOW_QUESTION QUESTION_HOLIDAY":
            return render_template("/hard_holiday.html")
        else:
            print("Quiz ended, the user answers were: ", answers)
            return render_template("/quiz_ended.html")

@app.route("/correct_answer")
def correct_answer():
    return render_template("correct_answer.html")

@app.route("/wrong_answer")
def wrong_answer():
    return render_template("wrong_answer.html")

@app.route('/endpoint', methods=['POST'])
def handle_request():
    global answers

    data = request.json.get('data')
    # Process the data as needed
    print("Data received from client:", data)
    # You can send a response back to the client if needed

    #saving user answers
    if data == "Correct answer" or data == "Wrong answer":
        update_answers(current_action, data)
    

    #ask planner what to do next
    if data == "True_son" or data == 'Quiz start':
        action, action_id = next_action(difficulty, last_action_id, True)
        update_actions(action, action_id)
        if action.split()[0] == "CHECK_ANSWER":
            start_evaluation(action)

    elif data == "False_son":
        action, action_id = next_action(difficulty, last_action_id, False)
        update_actions(action, action_id)
        if action.split()[0] == "CHECK_ANSWER":
            start_evaluation(action)

    

    return jsonify({'message': 'Data received successfully!'})


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return home()#'Server shutting down...'

# if __name__ == '__main__':
#     #We put debug=True in order to refresh the page every time a chage is made in the application
#     app.run(debug=True, host='127.0.0.1', port=9100)    


def start_server():
    app.run(debug=False, host='127.0.0.1', port=9100)

