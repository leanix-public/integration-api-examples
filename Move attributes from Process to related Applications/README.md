# UseCase:

Pick the highest businessCriticality from the related processes and apply to the Application.
If no businessCriticality is defined on any of the related processes the businessCriticality on Application is kept empty

# Additional consideration:

Question: What is the expectation when more than one Process is linked to an application, which Process should be considered Primary for picking this information?
Answer: Highest criticality must be checked from the related Processes and applied to the Application.

# Connector steps:
* Read relations Process to Application
    Read the relationship and add attributes to variables
    Also collect the ApplicationsIds into a variable where the update should be made.
* Write attributes to Applications
    Apply the variables read above to the ApplicationsIds