# UseCase:

This connector syncs subscriptions from a parent factsheet to it’s associated children.

# Connector steps:
* Read relations Process to Application
    Read the relationship and add attributes to variables
    Also collect the ApplicationsIds into a variable where the update should be made.
* Write attributes to Applications
    Apply the variables read above to the ApplicationsIds