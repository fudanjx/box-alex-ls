import os
import sys
import streamlit as st
import pandas as pd
import anthropic
import Anthropic_API

def main():
    """
    Main function to run the Long Stayer Analyzer web app.
    """
    st.title("Bot-Alex: Long Stayer Analyzer")
    st.text("- AI App to analyze what stop long stayer patients from discharge")

    with st.expander("###### AI Model Setup"):
        anthropic.api_key = st.text_input("Enter Anthropic API Key", type="password")
        os.environ['ANTHROPIC_API_KEY']= anthropic.api_key
        if not anthropic.api_key:
            st.warning('Press enter after you iput the API key to apply', icon="⚠️")     
        else:
            st.success('Model setup success!', icon="✅")      
    # Upload Patient Notes
    
    notes_file = st.file_uploader("Upload Anonymized Patient Notes", type=["csv"])
    
    # Analyze the long stayer
    if st.button("Analyze"):
        # Analyze
        result_note = pd.read_csv(notes_file)
        # Iterate over each row
        progress_text = "Analyzing in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        counter = len(result_note)
        each_run = 1/counter
        percent_complete = 0
        for index, row in result_note.iterrows():
            # Get the value from the 'anonymized notes' column
            Notes = row['Anonymized_NOTE_TEXT']
            generated_prompt = Anthropic_API.generate_prompt(Notes)
            # Call Anthropic_API.claude() with the generated prompt
            response = Anthropic_API.claude(generated_prompt)    
            # Store the response in the 'AI Results' column
            result_note.at[index, 'AI Results'] = response
            # subset_df = result_note[["Bed", "AI Results"]]
            my_bar.progress(percent_complete + each_run, text=progress_text)
            percent_complete += each_run
        st.success("Analysis completed!", icon="✅")
        download_results_df = result_note[['Bed', 'AI Results']]
        st.dataframe(download_results_df)
        
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')
        csv = convert_df(download_results_df)

        st.download_button(
        "Download",
        csv,
        "LongStayerResults.csv",
        "text/csv",
        key='download-csv'
        )
            

if __name__ == "__main__":

    # Run the main function
    main()
