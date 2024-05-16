
# Usage
BotApp must be deployed prior to AzureBot.

### Command line:
1. `az login`<br>
2. `az account set --subscription "<subscription>"`<br>
3. `az group create --name "<group>" --location "<region>"`<br>
4. `az ad app create --display-name "<app-registration-display-name>" --sign-in-audience "AzureADMyOrg"`<br>
5. `az ad app credential reset --id "<appId>"`. [Record values you'll need in later steps: the app ID and password from the command output]<br>
6. `az deployment sub create --template-file <template-file> --location <bot-region> --parameters <parameters-file>` [Perform this step twice, once for BotApp and AzureBot in the order mentioned]

## Parameters for template-BotApp-new-rg.json:

- **groupName**: (required)           The name of the new Resource Group.
- **groupLocation**: (required)       The location of the new Resource Group.
- **appServiceName**: (required)      The location of the App Service Plan.
- **appServicePlanName**: (required)  The name of the App Service Plan.
- **appServicePlanLocation**:         The location of the App Service Plan. Defaults to use groupLocation.
- **appServicePlanSku**:              The SKU of the App Service Plan. Defaults to Standard values.
- **appId**: (required)               Active Directory App ID or User-Assigned Managed Identity Client ID, set as MicrosoftAppId in the Web App's Application Settings.
- **appSecret**: (required for MultiTenant and SingleTenant)  Active Directory App Password, set as MicrosoftAppPassword in the Web App's Application Settings.

## Parameters for template-AzureBot-new-rg.json:

- **groupName**: (required)           The name of the new Resource Group.
- **groupLocation**: (required)       The location of the new Resource Group.
- **azureBotId**: (required)          The globally unique and immutable bot ID. Also used to configure the displayName of the bot, which is mutable.
- **azureBotSku**:                    The pricing tier of the Bot Service Registration. Allowed values are: F0, S1(default).
- **azureBotRegion**:                 Specifies the location of the new AzureBot. Allowed values are: global(default), westeurope.
- **botEndpoint**:                    Use to handle client messages, Such as `https://<botappServiceName>.azurewebsites.net/api/messages`.
- **appId**: (required)               Active Directory App ID or User-Assigned Managed Identity Client ID, set as MicrosoftAppId in the Web App's Application Settings.

7. Create a zip file from the contents within the code folder
8. `az webapp deployment source config-zip --resource-group "<resource-group-name>" --name "<name-of-app-service>" --src "<project-zip-path>"`