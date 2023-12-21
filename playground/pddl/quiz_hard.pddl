(define (problem quiz_hard)
    (:domain pepper_domain)

    (:objects
        question_1 - question
        question_swarm - question
        question_baseball - question
        question_mars - question
	)
	
	(:init
			(unknown (right_answer question_1))
			(unknown (right_answer question_swarm))
			(unknown (right_answer question_baseball))
            (unknown (right_answer question_mars))
            (difficulty_hard)
            (classification_done)
    )
    
    (:goal (quiz_ended))
)
