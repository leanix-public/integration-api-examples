# Smartsheet to LDIF

## Requirements
- python 3.x  
- smartsheet-python-sdk
- pyyaml

## Abstract
The purpose of this script is to extract data from Smartsheet, transform it to LeanIX Data Interchange Format (LDIF), and load it into a LeanIX workspace.  The relationship hierarchy is structured: Workspace / Sheet / Task / Subtask.  As a best practice, we do not want to have more than four layers in a hierarchy (although the script will allow it).  This connector is meant to be run as a Lambda/Azure function on a schedule, using a key store as best practice.  

## Setup
- Create a technical user in Smartsheet and LeanIX. 
- Share all desired Smartsheet workspaces and sheets with the integration user.
- Create an API token for the technical user in Smartsheet and LeanIX.  
- Ensure the config.yml has been configured with the desired field mapping, url's and log level. 
  - Any fields that contain spaces or special characters should be mapped to an API friendly name, e.g. "Project Phase": "projectPhase"
  - If adding fields to the field_mapper, they should also be added in the sh_processor.json where necessary.
  - See [LeanIX iAPI documentation](https://docs-eas.leanix.net/docs/inbound-processors) for help mapping new fields.      
- Insert key store code in sh_get_sheet.py on line 21, returning the Smartsheet API token.
- Insert key store code in sh_get_sheet.py on line 165, returning the LeanIX API token.
- Package the sh_processor.json and config.yml with sh_get_sheet.py and its dependendencies.  
- Implement on serverless infrastructure in your cloud of choice or on-prem.

## Current functionality
- list all workspaces, sheets, and sub/tasks
- extract data from all workspaces, sheets, and sub/tasks
- transform data to ldif
- load ldif into LeanIX workspace
