# UseCase:

Import Applications into LeanIX workspace with some basic information. Eg. Name,Description and Business Criticality

| Name                 |  Type  | 
|:---------------------|:------:|
| name                 | string |
| description          | string |
| businessCriticality  | choice |

Value mapping for Business Crticality

| External Value |  LeanIX Value         | 
|:---------------|:---------------------:|
| 1-Critical     | missionCritical       | 
| 2-High         | businessCritical      |
| 3-Low          | businessOperational   |
| 0-NonCritical  | administrativeService |