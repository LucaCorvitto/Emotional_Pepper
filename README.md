# Emotional_Pepper
Human Robot Interaction performed with a Pepper robot showing emotive reactions to the opinions of the user while collecting personal data.

## Description of the interaction
![image](https://github.com/LucaCorvitto/Emotional_Pepper/blob/main/images/flow_chart_report_single_page.png)

The process begins with the robot using its sonars to detect people. Upon detecting a person, Pepper checks their position and initiates interaction. If the user is unknown, Pepper introduces itself, gathers personal information, and updates its database. If the user is known, they are greeted, and Pepper may invite them to retake a quiz.

The interaction involves the robot asking questions, sharing information, and displaying emotive reactions based on the user's responses. The final phase includes presenting a quiz on Pepper's tablet, tailored to the user's robot approval level, with the robot adjusting its mood based on the quiz results.

The implementation includes an HTML server to emulate the tablet interaction, and the inclusion of emotive reactions aims to enhance the human-robot bond by creating a more natural and empathetic interaction.

## Demo
A video showing the complete interaction is available at this drive [link](https://drive.google.com/file/d/1a2gOVjcWnavSUrYpP0SXUduf76JHvr-5/view). For more detailed information it is available the [`report.pdf`](report.pdf).

## Code overview
![image](https://github.com/LucaCorvitto/Emotional_Pepper/blob/main/images/architecture_graph.png)
The project was implemented in the Ubuntu operating system, through Docker. The code was written mainly in Python, but PDDL, HTML, CSS and Javascript were also used for more specific tasks. We tested and carried out the simulation of the overall interaction on the [Choregraphe](http://doc.aldebaran.com/2-4/software/choregraphe/index.html) simulator and on the Firefox browser. The image above describes the architecture created to perform the interaction.

## Authors
[Luca Corvitto](https://github.com/LucaCorvitto)

[Lorenzo Faiella](https://github.com/FiscalTax)


