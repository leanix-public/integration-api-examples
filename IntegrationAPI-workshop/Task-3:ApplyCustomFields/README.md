# UseCase:

Import Applications into LeanIX workspace with some basic information. Eg. Name,Description and Business Criticality

| Name                 |  Type  | 
|:---------------------|:------:|
| name                 | string |
| description          | string |
| businessCriticality  | choice |

`config.json` file here provides an example on how to create an application. Enhance this with the below task.
Task 3: In this case leverage the customFields mapping defined in the `input.json` and use this defined to import the values.

Hint: Check the documentation for the usage of customFields : https://docs-eam.leanix.net/reference/advanced

| External Value |  LeanIX Value         | 
|:---------------|:---------------------:|
| 1-Critical     | missionCritical       | 
| 2-High         | businessCritical      |
| 3-Low          | businessOperational   |
| 0-NonCritical  | administrativeService |