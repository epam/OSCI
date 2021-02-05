# Azure Resource Manager (ARM) templates

This folder contains templates for deploying resources required for OSCI functions:

## Resources

### App Settings

__appsettings__ contains template for deploying Azure Function App settings.

You can edit `azuredeploy_parameters.json` or create your own `azuredeploy_parameters.<env>.json` files to customize settings.


### Deploying Azure Resource Manager (ARM) templates to the Azure

#### 1) Sign in your Azure account using PowerShell
#### 2) Create a resource group that serves as the container for the deployed resources with using web UI
#### 4) Deploying templates

   4.1) Fill fields in the files which has name like azuredeploy_parameters.json  <br>
   4.2) Fill the field after "ResourceGroupName" using your resource group name <br>
   4.3) Run the PowerShell script in the folder  <br>
   4.4) Repeat previous steps 4.1 and 4.2 for other resources  <br>
