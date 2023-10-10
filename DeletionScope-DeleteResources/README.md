# UseCase:

Sometimes it is not possible to remove the docs from the UI, example for the confluence integration links. Here you can use the attached connector to perfrom this deletion.
In addition in case there is a link which is available on a specific scope of factsheets, this can also be deleted by specific the scope and then in the advanced filter the parameter to be used. Eg. name/url


# Connector steps:
* DeletionScope deletes the factsheets on the basis of the below:-
    * FactSheetID specified in case this is very specific to a single record.
    * Filter applied in case FactSheetID is not specified.
    * Name of the resource should match with the one mentioned in the advanced filter.