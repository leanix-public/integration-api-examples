# UseCase:

This Connector demonstrates how tags from a single tag group can be propagated from a parent factsheet to a child factsheet. 
This example is implemented for Business Capbilities

# Connector steps:


* Line 28 - Filtering is set to only propagate tags from Factsheets NOT taged "L0 Platform"
* Line 68 & 76 - Children are filtered based on a target field Capability Type
* Line 110 - inboundTag for Capabilities leverages customFields to transform tags
* Line 146 - inboundTag for Capability Groups does NOT use customFields, therefore passing identical values