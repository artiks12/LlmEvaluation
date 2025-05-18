# LlmEvaluation
This is the repository to evaluate generated responses using LLM APIs. It is a part of the master thesis "Evaluation and Adaptation of Large Language Models for Question-Answering on Legislation" made in University of Latvia.

### How to Use
This script was used with Python 3.10 so it is recomended to use this version of python.

Since all packages needed are specified in notebook, there is no need to manually install them. 

You need is to put the generated responses that can be made here: https://github.com/artiks12/ResponseGeneration in ModelResponses folder.

Then do these steps:
- Run chatbotEvaluation.py script to prepare prompts for evaluation. They will be stored in instructions/SupervisedLlmEvaluation folder.
- Run GetModelEvaluatorResults notebook to get evaluations for responses. They will be stored in Scores/LlmEvaluatorAnswers folder.
- Run CalculateModelEvaluatorResults notebook to calculate average score for responses. They will be stored in Scores/LlmEvaluatorScores folder.

There might be some responses that make it more difficult to extract the scores as this code uses regular expressions to extract scores from the end of the text. Make sure to fix them by hand. The code is made in such way that scores cannot be extracted only for few responses. 
