[Setup continious export from ADX DBase Table to ADLSv2 (external table)](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/management/data-export/continuous-export-with-managed-identity?tabs=system-assigned%2Cazure-storage)
```console
.alter-merge cluster policy managed_identity ```[
    {
      "ObjectId": "system",
      "AllowedUsages": "AutomatedFlows"
    }
]```
```
System identity: 9dd3e9c8-xxxx-4311-xxx-xxxxxxxxxxxx

Give the System Managed Identity access to the database
.add database ['splunk-2-adx'] admins ('aadapp=9dd3e9c8-xxxx-4311-xxx-xxxxxxxxxxxx')

Create ADLSv2 and Container where data for the external table will reside
Assign Managed Identity to ADLSv2 Container [ADX -> Identity -> Add 'Storage Blob Data Contributor']

Create table in ADLSv2 container
Storage Account: "https://adxlogretention.blob.core.windows.net/splunktableext/m2131/data;impersonate" <br />
Table Schema's from internal table has to exactly match the external table you're creating
Existing internal table schema can be copied and directly applied to create the external table
Example:
```console
.show table Heartbeat cslschema
```
![BD918AE0-1407-4091-8EC7-A65CF26A75CC](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/4f9484fc-3c4d-4ef2-b55e-d1bfae328b4e)

Supported Data Formats: CSV, JSON, and PARQUET
```console
.create external table SplunkTableEXT (FWLogEntry:dynamic) kind=storage dataformat=parquet
( 
    h@'https://adxlogretention.blob.core.windows.net/splunktableext/m2131/data;impersonate' 
)
```

Create a continious export job from ADX -> ADLSv2
```console
.create-or-alter continuous-export SplunkTableExport over (SplunkTable) to table SplunkTableEXT with (managedIdentity="system", intervalBetweenRuns=5m) <| SplunkTable
```

ADX LOCAL TABLE QUERY
The internal and external tables should operate in the same manner with respect to KQL queries
```console
SplunkTable

SplunkTable
| extend t = parse_json(FWLogEntry)
| distinct TimeGenerated=todatetime(t.TimeGenerated), Company=tostring(t.Company), Hacker=tostring(t.Hacker), Venue=tostring(t.Venue), Type=tostring(t.Type)
```

ADLSv2 EXTERNAL TABLE QUERY
```console
external_table("SplunkTableEXT")

external_table('SplunkTableEXT')
| extend t = parse_json(FWLogEntry)
| distinct TimeGenerated=todatetime(t.TimeGenerated), Company=tostring(t.Company), Hacker=tostring(t.Hacker), Venue=tostring(t.Venue), Type=tostring(t.Type)
```
