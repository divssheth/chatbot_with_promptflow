from promptflow import tool
import requests
import json
from promptflow.connections import CustomConnection


def web_search(conn:CustomConnection, organization_urls: list, query: str):
    sites = organization_urls
    count = 3
    search_results = []
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    subscription_key = conn.secrets['bingapikey']

    for site in sites:
        #search_term = 'site:'+site+ ' ' + query
        search_term = query+' site:'+site
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        params = {"q": search_term, "count": count}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results.append(response.json()['webPages']['value'])
        # search_results.append(response.json())
    return search_results

@tool
def my_python_tool(question: dict, organization_urls: list, conn:CustomConnection) -> str:
  result = "The question is irrelevant or out of scope"
  query = json.loads(question)
  if query["relevance"]:
    result = web_search(conn, organization_urls, query["question"])
  return result
