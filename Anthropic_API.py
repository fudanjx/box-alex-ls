
import anthropic
import pandas as pd
import os


def open_file(filepath):
    with open(filepath, 'r') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w') as outfile:
        outfile.write(content)



def claude(instruct):
    client = anthropic.Client(os.environ["ANTHROPIC_API_KEY"])
    response = client.completion(
        prompt=instruct,
        # stop_sequences = [anthropic.HUMAN_PROMPT],
        model="claude-v1-100k",
        max_tokens_to_sample=4000,
        temperature=0
    )
    text = response['completion']
    return text

def generate_prompt(anonymized_notes):
    prompt = f"""{anthropic.HUMAN_PROMPT}: You are a medical officer
    {anthropic.HUMAN_PROMPT}: here we have patient's medical notes and inpatient documentation {anonymized_notes} 
    {anthropic.HUMAN_PROMPT}: Please help to analyze the patient's medical records and inpatient documentation to answer below questions 
    {anthropic.HUMAN_PROMPT}: Summarize briefly what are the main reason stop patient from discharge, and categorize into:
    {anthropic.HUMAN_PROMPT}: 1. Whether patient is medically fit to discharge. 2. Caregiver issue 3. Financial related issue 4. other issue 5. patient ready to go home
        \n\n{anthropic.AI_PROMPT}:\n\n"""
    return prompt


    
