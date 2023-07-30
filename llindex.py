import os
from pathlib import Path
from typing import Dict, List, Optional

import openai
import pandas as pd
import requests

import html2text
import llama_index
from llama_index import GPTVectorStoreIndex, download_loader
from llama_index.readers.schema.base import Document
from llama_index import SimpleWebPageReader, QuestionAnswerPrompt
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

path = '/Users/bseetharaman/Desktop/FY23/TPF_Hackathon/file.csv'


import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import io
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive']


class LL_INDEX:
    def __init__(self): 
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def _validate_prompt_template(self, prompt_template: str):
            if '{context_str}' not in prompt_template or '{query_str}' not in prompt_template:
                raise Exception("Provided prompt template is invalid, missing one of `{context_str}` or `{query_str}`. Please ensure both placeholders are present and try again.")  
    
    def load_pdf_data(self):
        """Parse file."""
        import pypdf

        import os
        import glob

        directory_path = '/Users/bseetharaman/Desktop/FY23/TPF_Hackathon/documents/hr'

        pdf_files = []
        for file in glob.glob(os.path.join(directory_path, '*.pdf')):
            pdf_files.append(file)
        
       
        docs = []
        print("List of PDF files in the directory:")
        for file in pdf_files:

            with open(file, "rb") as fp:
                pdf = pypdf.PdfReader(fp)
                num_pages = len(pdf.pages)
               
                for page in range(num_pages):
                    page_text = pdf.pages[page].extract_text()
                    page_label = pdf.page_labels[page]
                    metadata = {"page_label": page_label, "file_name": file}

                    docs.append(Document(text=page_text, extra_info=metadata))

        return docs
    
    def load_jira_data(self):

        if os.path.exists(path):
            jira_issues_df = pd.read_csv(path)
        
        else:
            s = requests.Session()
            s.headers['Authorization'] = 'Bearer NDU4OTIzMDE2MTgxOkU5CjVFV7L01piwU8WDYiEwuiOL'

            jira = Jira(url='https://jira.linuxfoundation.org/', session=s)
            query = 'project = RELENG'
            project = 'RELENG'
            count = jira.get_project_issues_count(project)
            print(count)
            count = 10
            data = []
            jql= 'project = RELENG'
            startAt = 0
            maxResults = 10
            total = 1
            fields = ["key", "fields.summary","fields.status.name", "fields.reporter.name","fields.assignee.name","fields.priority.name"]
            jira_issues_df = pd.DataFrame(columns=fields)
            print(jira_issues_df)
            while startAt <= total:      

                    print('Requesting jira data... ' + str(startAt) + ' from ' + str(total))
                    results = jira.jql(query,start=startAt,limit=maxResults)
                    df = pd.json_normalize(results["issues"])
                    df = df[fields]
                    # df = pd.json_normalize(res["issues"])
                    #jira_issues_df = pd.concat[jira_issues_df,df]
                    startAt += maxResults
                    total = count 
                    jira_issues_df = pd.concat([jira_issues_df, df], axis=0)

            print(jira_issues_df)

        documents = []
        for item in jira_issues_df.itertuples():
            doc_str = ", ".join([str(entry) for entry in item])
            print(doc_str)
            documents.append(Document(text=doc_str))

    
       
        return documents

    
    
    def load_url_data(self):
        documents = []
        
        urls = ['https://hack2skill.com/hack/gen-ai-rush-buildathon/','https://mindsdb.com/about']
        for url in urls:
            response = requests.get(url, headers=None).text            
            response = html2text.html2text(response)
            documents.append(Document(text=response))

        return documents
    

    def fetch_file(self):
        """Insert new file.
        Returns : Id's of the file uploaded

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # create drive api client
            service = build('drive', 'v3', credentials=creds)

            file_metadata = {'name': 'output.pdf'}
            media = MediaFileUpload('output.pdf',
                                    mimetype='application/pdf')
            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, media_body=media,
                                        fields='id').execute()
            print(F'File ID: {file.get("id")}')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None
        
        url = f"https://drive.google.com/file/d/{file.get('id')}/view?usp=sharing"

        return url


    def fetch_file_output(self, prompt):
        docs_url = self.fetch_file()
        return(docs_url)


    def fetch_url_qa_output(self, prompt):
        docs = self.load_url_data()
        index = GPTVectorStoreIndex.from_documents(docs)
        query_engine = index.as_query_engine()
        query_results = query_engine.query(prompt)
        return(query_results)

    def fetch_jira_qa_output(self, prompt):
        docs = self.load_jira_data()
        index = GPTVectorStoreIndex.from_documents(docs)
        query_engine = index.as_query_engine()
        query_results = query_engine.query(prompt)
        return(query_results)

    
    def fetch_hr_qa_output(self, prompt):
        docs = self.load_pdf_data()
        index = GPTVectorStoreIndex.from_documents(docs)
        query_engine = index.as_query_engine()
        query_results = query_engine.query(prompt)
        return(query_results)
    
    def fetch_openai_output(self, prompt):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  
                prompt=prompt,
                max_tokens=100  
            )
            return response['choices'][0]['text'].strip()
        except openai.error.AuthenticationError:
            return "Authentication error. Please check your API key."
        except openai.error.RateLimitError:
            return "Rate limit exceeded. Please wait a while and try again."
        except openai.error.APIError as e:
            return f"OpenAI API error: {e}"
    
if __name__ == "__main__":
    llindex = LL_INDEX()
    prompt_text = "what is maximum amount for Educational & Learning Reimbursement?"
    output = llindex.fetch_hr_qa_output(prompt_text)
    
    # output = llindex.fetch_openai_output(prompt_text)
    print(output)

