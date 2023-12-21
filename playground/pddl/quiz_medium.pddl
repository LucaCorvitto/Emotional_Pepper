(define (problem quiz_hard)
    (:domain pepper_domain)

    (:objects
        question_manufactured - question
        question_swarm - question
        question_guinness - question
        question_mars - question
	)
	
	(:init
			(unknown (right_answer question_manufactured))
			(unknown (right_answer question_swarm))
			(unknown (right_answer question_guinness))
            (unknown (right_answer question_mars))
            (difficulty_medium)
            (classification_done)
    )
    
    (:goal (quiz_ended))
)
