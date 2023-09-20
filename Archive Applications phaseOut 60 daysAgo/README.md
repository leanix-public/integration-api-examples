# UseCase:

In case customers want to do a cleanup of the Applications and remove the applications which are phasedOut 60 days ago.

# Additional consideration:

This can be easily adapted for other FactSheets and lifecycle phases by adapting the scope.

# Connector steps:
* Uses deletionScope to archive the FactSheets.
* Create the Connector in the Full Mode to leaverage this config.
* Test this in the Sandbox first if you get the expected results.
* Modify the part integration.now.minusDays(60) as per your needs.