from pathlib import Path
from llama_index import GPTVectorStoreIndex
from typing import Dict, List, Optional
from atlassian import Jira
import pandas as pd
import requests
import os

path = '/Users/bseetharaman/Desktop/FY23/TPF_Hackathon/file.csv'
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


def safe_value_dict(dict_obj):
    for key, value in dict_obj.items():
        if isinstance(value, (str, int, float)):
            dict_obj[key] = value
        elif isinstance(value, list):
            # Convert lists to strings
            dict_obj[key] = ", ".join(map(str, value))
        elif value is None:
            # Replace None with a default string
            dict_obj[key] = ""
        else:
            # Convert other types to strings
            dict_obj[key] = str(value)
    return dict_obj




class JIRAReader(BaseReader):
    """JIRA reader."""
  
    
    def load_data():
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


        
docs = JIRAReader.load_data()
print(docs)


index = GPTVectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()
query_results = query_engine.query("what are the jiras assigned to kevin.sandi?" )
#query_results = query_engine.query("what is maximum amount for Educational & Learning Reimbursement?")
#query_results = query_engine.query("How many sick leaves an employee is eligible for?")


print(query_results)
