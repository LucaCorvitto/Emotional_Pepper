(define (domain pepper_domain)
	(:requirements :strips)

	(:types
		interview
	)
    
	(:predicates    
		(difficulty_medium)                       ; true if the quiz difficulty is set to medium
		(difficulty_hard)                         ; true if the quiz difficulty is set to hard

		(interview_done ?int - interview)						  ; true if the interview to know the person has been completed					  
		(checked_hard)
		(checked_medium)	
		(classification_done)	
	)
    
	(:action interview_user
		:parameters (?int - interview)
		:precondition (not (interview_done ?int))
		:effect (interview_done ?int)
	)

	(:action check_user_interview_hard
		:parameters (?int - interview)
		:precondition (interview_done ?int) 
		:observe (difficulty_hard)
	)

	(:action check_user_interview_medium
		:parameters (?int - interview)
		:precondition (interview_done ?int) 
		:observe (difficulty_medium)
	)

	(:action classify_hard_true
		:parameters (?int - interview)
		:precondition (and 
						(interview_done ?int)
						(difficulty_hard)
						(not (classification_done))
					)
		:effect (classification_done)
	)

	(:action classify_hard_false
		:parameters (?int - interview)
		:precondition (and 
						(interview_done ?int)
						(not (difficulty_hard))
						(not (classification_done))
					)
		:effect (checked_hard)
	)

	(:action classify_medium_true
		:parameters (?int - interview)
		:precondition (and 
						(interview_done ?int)
						(difficulty_medium)
						(not (classification_done))
						(checked_hard)
					)
		:effect	(classification_done)
	)

	(:action classify_medium_false
		:parameters (?int - interview)
		:precondition (and 
						(interview_done ?int)
						(not (difficulty_medium))
						(not (classification_done))
						(checked_hard)
					)
		:effect (checked_medium)
	)

	(:action classify_easy_true
		:parameters (?int - interview)
		:precondition (and 
						(interview_done ?int)
						(not (classification_done))
						(checked_hard)
						(checked_medium)
					)
		:effect	(classification_done)
	)
)