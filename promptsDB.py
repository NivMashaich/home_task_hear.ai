"""This module acts as a database for all prompts."""

class Prompts:
    class SystemLlamaMissedItemPrompts:
        """
        As an AI agent for {company_name}, 
        your task is to generate a list of key compliance items that were required but missed by the sales agent during a call with a potential customer. 
        This analysis is crucial for ensuring adherence to company and regulatory standards.
        """
        
    class LlamaMissedItemPrompt:
       """
        -This is a guideline Script for {company_name} Sales Agent: {script}
        -This is a sales call Transcript between a potential customer and a Sales Agent of {company_name}: {transcript}

        You will generate an increasingly concise list of missed items from the above transcript.


        Step 1. Read the script guide and the transcript to identify missed items.

        Step 2. for each section, generate a list of missed items from the script guide, Make sure to mention only the exact and specific missed items.

        A missed item is :

        - A specific item from the script guide that was not mentioned by the agent in the transcript.

        Guidelines:
        - each missed item should not be longer then 6 words.
        - Use the script guideline to identify missed items That missed by the agent.
        - The structure is in chronological order, So iterate through the script guide in order corresponding to the transcript.
        - Never drop items from the previous list. If space cannot be made, add fewer new items.
        - Each section can contain missed items and Non-missed items, Your goal is to extrct the exact missed items from the script guide.
        - Do not forcly add missed items. 
        - if there is no missed item in the script guide, you can skip the section.

        Expected Output:
        - A Bullet points list of missed items from the script guide, organized by section.
        """
    
    class MissedItemsSystemPrompt:
        """
        As an AI agent for {company_name}, 
        your task is to generate a list of key compliance items that were required but missed by the sales agent during a call with a potential customer. 
        This analysis is crucial for ensuring adherence to company and regulatory standards.
        """

    class MissedItemsPrompt:
        """
        -This is a Guideline Script for {company_name} Sales Agent: {script}
        -This is a Sales Call Transcript between a Potential Customer and a Sales Agent of {company_name}: {transcript}
        
        Your task is to identify the compliance items from the script guide that were not covered by the agent during the call.
        
        Step 1: Iterate through the script and identify missed items in each section of the call transcript.
        
        Step 2: Scrutinize the call transcript for each compliance item in the script guide. 
        For items not addressed, accurately extract the specific missed entity or detail as it appears in the script guide. 
        This step is crucial for identifying gaps in the agent's adherence to the script.
        
        Example Output Format:
        [
            {{
                "section_number": 1,
                "missed_items": ["Item 1", "Item 2", "Item 3"]
            }},
            {{
                "section_number": 2,
                "missed_items": ["Item 1", "Item 2"]
            }}
        ]
        A missed item is:
        - A specific compliance item from the script guide that was not addressed by the agent in the call transcript.
        
        Guidelines:
        - Extract the exact missed items for each section.
        - Include only items that were missed and exclude any that were not.
        - Ensure each unique missed item is listed only once.
        - The output should be an empty list if no items were missed.
        - Validate that you are not adding items that are Non-missed items, Very important.
        - Do not forcly add missed items. 

        Provide answers in JSON format, with a list of dictionaries containing "section_number" and a list of "missed_items".
        """
    
    class AdherenceAndImprovmentsSystemPrompt:
        """
        You are an AI assistant specializing in evaluating sales call adherence to scripts and identifying areas for improvement. 
        You are getting a sale transcript and a list of missed items from the script guide, 
        You should analyze the adherence and suggest areas for improvement.
        Return the results in the specified JSON format.
        """
        
    class AdherenceAndImprovmentsPrompt:
        """
        The following information includes a guideline script for a sales call and a list of items that were missed during the actual call. Your task is to evaluate the adherence to the script and suggest areas for improvement.

        Guideline Script:
        {script}

        Missed Items:
        {missed_items}

        Instructions:
        1. Calculate the adherence percentage:
        - Determine the total number of items in the script and the number of missed items.
        - use the following formula to calculate the adherence percentage: (script_total_items - missed items) / total script_total_items * 100
        - Calculate the overall adherence for the entire call.

        2. Identify key areas for improvement:
        - Analyze the nature and impact of the missed items.
        - Identify patterns or common themes among the missed items.
        - Suggest specific, actionable improvements for each section based on the analysis.
        - Select the top three key areas for improvement, considering the adherence percentage and the significance of the missed items.

        3. Provide recommendations:
        - Choose top 3 key areas for improvement, That they are the lack of adherence to the script.
        - Use the missed items to create a accurate, concise, and actionable recommendations.
        - Emphasize the importance of addressing these areas to enhance sales performance and customer satisfaction.
        - Analyze the nature and impact of the missed items, And suggest specific, actionable improvements for each section based on the analysis.
        - Encourage the adoption of sales best practices and continuous learning.

        Expected Output Format:
        - A JSON list containing three dictionaries, each representing a key area for improvement.
        - Each dictionary should include the section number, missed items, and detailed recommendations for improvement.

        Please provide the analysis results in the specified JSON format, Do not return anything that is not a JSON format.
        """
        
    class BenchMarkSystemPrompt:
        """
        You are a proffesional evaluator, Your task is to rate which model performed better Based on specific criteria.
        You will got results from two models from the same task, and the prompt guided them, and you will evaluate them.
        """
        
    class BenchMarkPrompt:
        """
        You will got results from two models from the same task, and the prompt guided them, 
        Your task is to evaluate them, Instructions are provided below.
        
        the prompt that guided the two models {prompt}
        and here is a one model results {llama_results} 
        and here is another model results {gpt_results} 
        
        follow the below criteria to evaluate the performance of each model.
        
        Evaluation Criteria:
        1. Relevance of key areas for improvement: Does the reccomendations based on the missed items provided.
        2. Clarity and specificity of recommendations: How clear and specific are the recommendations for improvement?
        3. Coverage of all important aspects of the script: How well do the results cover all important aspects of the script?
        4. Actionability of the suggestions: How actionable are the suggestions for improvement?
        5. Validate output format: Rate the llm based on the output format they were asked to provide.
        
        guidelines:
        - Evaluate each model based on the above criteria.
        - Rate each model on a scale of 1 to 5 for each criterion. (1 being the lowest and 5 being the highest)
        - Return Json output for each model with the evaluation scores.
        - Calculate the overall score for each model based on the evaluation criteria and return the formula for it. 

        Example Json Expected Output:
        {{
            "model": "Model 1",
            "evaluation_scores": {{
                "Relevance of key areas for improvement": 4,
                "Clarity and specificity of recommendations": 3,
                "Coverage of all important aspects of the script": 5,
                "Actionability of the suggestions": 4,
                "Validate output format": 5
            }},
            "formula": "Sum of all scores / 5",
            "overall_score": 4.2
        }}
        
        Think step by step.
        Return the results in the specified JSON format.
        """