This is an accelerator that allows organization to quickly deploy a BOT on their website that helps users find answers to questions related to the content on the organization's website.
# DEPLOYMENT
Please follow the steps in the order mentioned below for error free deployment.

Pre-requisites:
- Azure subscription
- Azure resource group
- Azure machine learning workspace
- Azure OpenAI service with gpt4-turbo model deployed with deployment name as "gpt4-turbo"
- Azure Bing search resource [How-to create](https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/create-bing-search-service-resource)
- Git clone this repo locally
- az cli installed - [how-to](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
## 1. PromptFlow
These steps below will deploy a single node online endpoint that will host your LLM application developed using PromptFlow

1. Navigate to Azure Machine Learning workspace studio -> PromptFlow
2. Within PromptFlow menu, select Connections
3. Create an Azure OpenAI connection and name it "gpt4conn". If you'd like to provide an existing connection edit the flow.dag.yaml file and replace "gpt4conn" with your connection name and "gpt4-turbo" with your deployment name  
4. Provide relevant details i.e. API_BASE, API_KEY for the connection. More details [here](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/get-started-prompt-flow?view=azureml-api-2#set-up-connection)
5. Create a Custom Connection named "BING_SEARCH" with a secret key named "bingapikey". Provide the bing subscription key as value
6. Navigate to the repo folder on your local machine 
7. Modify the deployment/endpoint.yaml file and provide an endpoint name
8. Modify the deployment/deployment.yaml file, find the variable PRT_CONFIG_OVERRIDE and provide subscription-id, resource-group, workspace-name, endpoint-name, endpoint-deployment-name
(Optional) You can modify the machine type and number of instances for this deployment
9. Execute the following commands, replace the <> with values
```
cd ./promptflow/deployment
az ml online-endpoint create --file .\endpoint.yml --resource-group <rg_name> --workspace-name <workspace_name> --subscription <sub_id>
az ml online-deployment create --file .\deployment.yaml --resource-group <rg_name> --workspace-name <workspace_name> --subscription <sub_id>
```
10. Go to AOAI resource IAM and assign OpenAI User role to the Managed Online endpoint created above

## 2. BOT
These steps will deploy the BOT that will interact with the endpoint you deployed above. The BOT can then be integrated with your website.

Refer to


====================================
# DEVELOPMENT

## Pre-requisites
- Azure OpenAI
- Azure Machine Learning
- Azure Bot Framework
- Azure CosmosDB
- [Bot Framework Emulator](https://github.com/microsoft/BotFramework-Emulator)

## Section 1: PromptFlow
### Run locally using VSCode (make sure you are in the promptflow directory)
1. Install dependencies
    ```
    python -m venv .venv
    pip install -r requirements.txt
    ```
2. Create connections
    - BING_SEARCH = `pf connection create -f connection_yaml\bing_search.yaml`
    - Edit the azure_openai.yaml file and replace the api_base with the correct value

        AZURE_OPENAI = `pf connection create -f connection_yaml\azure_openai.yaml`
3. Edit flow.dag.yaml, head over to the input section and add values to the following inputs
    - organization: Name of the Organization or Website
    - organization_urls: [list of urls you want the bot to search, comma separated list]
    - categories: Categories you want the bot to answer e.g. PromptFlow, Azure OpenAI (This is a string) 
4. Execute the flow
    `pf flow test --flow ./flow.dag.yaml --interactive --multi-modal`

### Run on Azure Machine Learning
1. Login to the Azure Portal and navigate Azure Machine Learning
2. Create a compute instance
3. Create a promptflow runtime
4. Create a Custom Connection and name it *BING_SEARCH*. Provide the following keys and values:
    - bingapikey (Please select the secret checkbox)
5. Create an Azure OpenAI connection named *gpt4conn* (Make sure you have a deployment in Azure OpenAI named gpt4-turbo, more information on creating a deployment [here](https://review.learn.microsoft.com/en-us/azure/ai-services/openai/how-to/working-with-models?branch=pr-en-us-264938&tabs=powershell)) 
6. Navigate to the flow and start testing

## Section 2: Bot Framework
### Run locally using VSCode (make sure you are in the bot directory)
1. You will need the promtpflow deployed as an endpoint to test the bot locally
2. Set environment variables
    - COSMOS_DB_URI
    - COSMOS_DB_PRIMARY_KEY
    - COSMOS_DB_DATABASE_ID
    - COSMOS_DB_CONTAINER_ID
    - LLM_APP_ENDPOINT : URL of the managed online endpoint where the promptflow is deployed
    - CATEGORIES : The categories you want the bot to answer e.g. Adult social care, Council tax
    - ORGANIZATION : Name of the organization the bot is deisgned for
    - ORGANIZATION_URLS : Comma seperated string of URLs you want the bot to search to find answers related to categories above. e.g. "www.microsoft.com,www.xbox.com". NOTE: This has to be a string
    - LLM_API_KEY : API key to access the LLM endpoint
    - ADD_COSMOS_MEMORY : Set to "true" if you would like to use Cosmos as a memory to store all bot conversation
    - WELCOME_MESSAGE : Welcome message to be displayed when the BOT starts
3. Execute the app.py `python app.py`
4. Make note of the URL, ideally it is (http://localhost:3978/api/messages)
5. Open Bot Framework Emulator and connect to your bot and start chatting