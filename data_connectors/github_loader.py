import requests
# import openai
# import os
from llama_index.readers.schema.base import Document
github_username = "bala-ceg"
access_token = "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"
repo_owner = "mindsdb"
repo_name = "mindsdb"
from llama_index import GPTVectorStoreIndex


def get_open_issues_with_assignee(repo_owner, repo_name, access_token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "state": "open",
        "per_page": 10
    }

    response = requests.get(url, headers=headers, params=params)
    docs = []
    if response.status_code == 200:
        issues = response.json()
        for issue in issues:
            assignee = issue['assignee']
            assignee_name = assignee['login'] if assignee else 'Unassigned'
            item = [[issue['number'],issue['title'],assignee_name]]
            doc_str = ", ".join([str(entry) for entry in item])
            docs.append(Document(text=doc_str))
        return (docs)

    else:
        print(f"Failed to fetch issues. Status code: {response.status_code}")
        print(response.json())


docs = get_open_issues_with_assignee(repo_owner, repo_name, access_token)
print(docs)
index = GPTVectorStoreIndex.from_documents(docs)
print(index)
query_engine = index.as_query_engine()
print(query_engine)
query_results = query_engine.query("what are the open issues assigned to ea-rus?" )
print(query_results)

