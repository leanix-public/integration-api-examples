# UseCase:

Import Applications into LeanIX workspace with some basic information. Eg. Name,Description and Business Criticality

| Name                 |  Type  | 
|:---------------------|:------:|
| name                 | string |
| description          | string |
| businessCriticality  | choice |

`config.json` file here provides an example on how to create an application. Enhance this with the below task.
Task 2: Use the Value mapping for Business Crticality to import the attribute into Application

Hint: Check the documentation : https://docs-eam.leanix.net/reference/inbound-processors#inbound-fact-sheet

| External Value |  LeanIX Value         | 
|:---------------|:---------------------:|
| 1-Critical     | missionCritical       | 
| 2-High         | businessCritical      |
| 3-Low          | businessOperational   |
| 0-NonCritical  | administrativeService |