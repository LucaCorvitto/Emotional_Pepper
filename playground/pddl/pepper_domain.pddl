(define (domain pepper_domain)
	(:requirements :strips)

	(:types 
		question
	)
    
	(:predicates    
		(right_answer ?x - question)   			  ; true if the user chooses the right answer to question x
		(question_answered ?x - question)  		  ; true if the user answered the question
		(difficulty_easy)						  ; true if the quiz difficulty is set to easy
		(difficulty_medium)                       ; true if the quiz difficulty is set to medium
		(difficulty_hard)                         ; true if the quiz difficulty is set to hard
		(quiz_started)
		(quiz_ended)						      ; true if the quiz has ended

		(classification_done)						  ; true if the interview to know the person has been completed					  

	)
    
	(:action check_answer
		:parameters (?q1 - question)
		:precondition (and
			(not (quiz_ended))
			(question_answered ?q1)
		)
		:observe (right_answer ?q1)
	)

	(:action quiz_start
		:precondition (not (quiz_ended))
		:effect (quiz_started)
	)

	; The robot shows the question on the tablet. 
	; The user chooses an answer. Pepper has to observe if the right answer was chosen.
	(:action show_question
		:parameters (?q - question)
		:precondition (and 
						(quiz_started)
						(not (quiz_ended))
						(classification_done)
					) ; :observe (right_answer ?q)
		:effect (question_answered ?q)
	)

	; The robot shows a final emotional response at the end of the quiz
	; if the quiz was easy 2/4 right answers make the robot happy
	; more then 2 wrong, robot is sad (easy)
	(:action sad_emotional_response_easy
		:parameters (?q1 - question ?q2 - question ?q3 - question ?q4 - question)
		:precondition (and 
						(difficulty_easy)
						(and
							(not (= ?q1 ?q2)) (not (= ?q1 ?q3)) (not (= ?q1 ?q4)) 
							(not (= ?q2 ?q3)) (not (= ?q2 ?q4)) (not (= ?q3 ?q4))
						)
						(and
							(question_answered ?q1)
							(question_answered ?q2)
							(question_answered ?q3)
							(question_answered ?q4)
						)
						(and 
							(not (right_answer ?q1))
							(not (right_answer ?q2))
							(not (right_answer ?q3))
						)	
					)
		:effect (quiz_ended)
	)
	; at least 2 correct, robot is happy (easy)
	(:action happy_emotional_response_easy
		:parameters (?q1 - question ?q2 - question ?q3 - question ?q4 - question)
		:precondition (and 
						(difficulty_easy)
						(and
							(not (= ?q1 ?q2)) (not (= ?q1 ?q3)) (not (= ?q1 ?q4)) 
							(not (= ?q2 ?q3)) (not (= ?q2 ?q4)) (not (= ?q3 ?q4))
						)
						(and
							(question_answered ?q1)
							(question_answered ?q2)
							(question_answered ?q3)
							(question_answered ?q4)
						)
						(and
							(right_answer ?q1)
							(right_answer ?q2)
						)
					)
		:effect (quiz_ended)

	)

	; if the quiz was medium 3/4 right answers make the robot happy
	; more then 1 wrong, robot is sad (medium)
	(:action sad_emotional_response_medium
		:parameters (?q1 - question ?q2 - question ?q3 - question ?q4 - question)
		:precondition (and 
						(difficulty_medium)
						(and
							(not (= ?q1 ?q2)) (not (= ?q1 ?q3)) (not (= ?q1 ?q4)) 
							(not (= ?q2 ?q3)) (not (= ?q2 ?q4)) (not (= ?q3 ?q4))
						)
						(and
							(question_answered ?q1)
							(question_answered ?q2)
							(question_answered ?q3)
							(question_answered ?q4)
						)
						(and 
							(not (right_answer ?q1))
							(not (right_answer ?q2))
						)	
					)
		:effect (quiz_ended)
	)
	; at least 3 correct, robot is happy (medium)
	(:action happy_emotional_response_medium
		:parameters (?q1 - question ?q2 - question ?q3 - question ?q4 - question)
		:precondition (and 
						(difficulty_medium)
						(and
							(not (= ?q1 ?q2)) (not (= ?q1 ?q3)) (not (= ?q1 ?q4)) 
							(not (= ?q2 ?q3)) (not (= ?q2 ?q4)) (not (= ?q3 ?q4))
						)
						(and
							(question_answered ?q1)
							(question_answered ?q2)
							(question_answered ?q3)
							(question_answered ?q4)
						)
						(and
							(right_answer ?q1)
							(right_answer ?q2)
							(right_answer ?q3)
						)
					)
		:effect (quiz_ended)
	)

	; if the quiz was hard 4/4 right answers make the robot happy
	; 1 wrong, robot is sad (hard)
	(:action sad_emotional_response_hard
		:parameters (?q1 - question ?q2 - question ?q3 - question ?q4 - question)
		:precondition (and 
						(difficulty_hard)
						(and
							(question_answered ?q1)
							(question_answered ?q2)
							(question_answered ?q3)
							(question_answered ?q4)
						)
						(and
							(not (= ?q1 ?q2)) (not (= ?q1 ?q3)) (not (= ?q1 ?q4)) 
							(not (= ?q2 ?q3)) (not (= ?q2 ?q4)) (not (= ?q3 ?q4))
						)
						(not (right_answer ?q1))
					)
		:effect (quiz_ended)
	)
	; all 4 correct, robot is happy (hard)
	(:action happy_emotional_response_hard
		:parameters (?q1 - question ?q2 - question ?q3 - question ?q4 - question)
		:precondition (and 
						(difficulty_hard)
						(and
							(question_answered ?q1)
							(question_answered ?q2)
							(question_answered ?q3)
							(question_answered ?q4)
						)
						(and
							(not (= ?q1 ?q2)) (not (= ?q1 ?q3)) (not (= ?q1 ?q4)) 
							(not (= ?q2 ?q3)) (not (= ?q2 ?q4)) (not (= ?q3 ?q4))
						)
						(and 
							(right_answer ?q1)
							(right_answer ?q2)
							(right_answer ?q3)
							(right_answer ?q4)
						)	
					)
		:effect (quiz_ended)
	)
)

  
  

