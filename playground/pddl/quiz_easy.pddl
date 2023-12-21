(define (problem quiz_hard)
    (:domain pepper_domain)

    (:objects
        question_name - question
        question_made - question
        question_moon - question
        question_guinness - question
	)
	
	(:init
            (unknown (right_answer question_name))
            (unknown (right_answer question_moon))
            (unknown (right_answer question_made))
            (unknown (right_answer question_guinness))
            (difficulty_easy)
            (classification_done)
    )
    
    (:goal (quiz_ended))
)
