# UseCase:

IF Approval Status == Approved for an Application and Lifecycle.active is empty set lifecycle.active to current date.

# Additional consideration:

Attribute approvalStatus with value Approved should be available on the Application Factsheet.

# Connector steps:
* Read approvalStatus and lifecycle for the current Application
    Apply the condition such that: 
        IF (approvalStatus = Approved and lifecycle.active is empty):
            Apply the current date
        ELSE
            Apply the lifecycle.active