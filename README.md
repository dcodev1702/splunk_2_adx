# Splunk-2-ADX (Azure Data Explorer) Data Migration
Python demo using Kusto SDK to ingest to and query from ADX Database (Table|SplunkTableRaw)

## [How-To](https://learn.microsoft.com/en-us/azure/data-explorer/ingest-json-formats?tabs=python):
0. Log into Azure with the required permissions / access
1. Create App Registration & Secret from Entra ID
2. Record Client_ID, Client_Secret, and Tenant_ID from App Registration
3. Create ADX Cluster
4. Create a Database within your ADX Cluster
5. Enable Managed Identity (System) for you ADX Cluster
6. Within the Database -- Assign "Admin permission" to App Registration
7. Create Tables, Mapping, and Expand function within ADX Database
8. [Install Python 3.X](https://www.python.org/downloads/) w/ the Kusto Python SDK (Windows / Linux / MacOS)
   ```console
      mkdir adx_demo
      python -m venv adx_demo
      source adx_demo/bin/activate
   ```
   ```console
      pip install azure-kusto-data
      pip install azure-kusto-ingest
   ```
   
## Illustration
### Ingestion: Kusto Python SDK used to programmatically authenicate & ingest data [data_ingest_all.json]
Sample Data (JSON): data_ingest_all.json
![F4B8A04B-4A14-4A25-9C99-DB780405A847](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/3f9ff3ff-6188-4273-b68c-bbf4962957f9)

![B971EE3A-9529-4C7F-A44B-0ADE92ECADC7](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/dde41858-c3b5-4612-baf8-04dcce81b233)

### ADX Database Query (SplunkTable) via Kusto Python SDK
![image](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/40b61863-2b81-4e0b-add7-22881bb7473d)

### ADX Database Query (SplunkTable) via ADX
![image](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/812b5597-70cd-4363-a5d4-0e4d07cbee0e)

Create temp table where data will ingest to
```console
.create table SplunkTableRaw (Records:dynamic)
```
$.FWLogEntry <-> MUST MATCH THE JSON OBJECT GETTING INGESTED FROM THE SOURCE [JSON FILE]!! <br />
FWLogEntry gets MAPPED TO THE "RECORDS" COLUMN of the SplunkTableRaw Table <br />
```console
// e.g. {"FWLogEntry":{"TimeGenerated":"2024-03-13T18:45:54.9122018Z", "Company":"MFCC-G9-DOG", "Hacker":"Maj JJ Bottles", "Venue":"BSides DC", "Type":"SplunkTable"}}
.create table SplunkTableRaw ingestion json mapping 'SplunkTableMapping' '[{"column":"Records", "Properties":{"Path":"$.FWLogEntry"}}]'
```
```console
.alter-merge table SplunkTableRaw policy retention softdelete = 0d
```

Create table (SplunkTable) where the data will reside
```console
.create table SplunkTable (FWLogEntry:dynamic)
```

Create SplunkTableExpand() function
```console
.create-or-alter function SplunkTableExpand() {
    SplunkTableRaw
    | project Records
}
```

Apply SplunkTableExpand() function to the SplunkTable
```console
.alter table SplunkTable policy update @'[{"Source": "SplunkTableRaw", "Query": "SplunkTableExpand()", "IsEnabled": true, "IsTransactional": true}]'
```
If you ever need to drop the SplunkTable or the SplunkTableExpand() Function
```console
//.drop function SplunkTableExpand
//.drop table SplunkTable ingestion json mapping "SplunkTable_JSON_Mapping"
```

Test data to ingest and ensure the tables, policies, mapping, and expand function is operating correctly. 
```console
.ingest inline into table SplunkTable with (format = "json") <| {"FWLogEntry":{"TimeGenerated":"2024-03-13T18:45:54.9122018Z", "Company":"MFCC-G9-DOG", "Hacker":"Maj JJ Bottles", "Venue":"BSides DC", "Type":"SplunkTable"}}
```

Query SplunkTable
```console
SplunkTable
| extend t = parse_json(FWLogEntry)
| project TimeGenerated=todatetime(t.TimeGenerated), Company=tostring(t.Company), Hacker=tostring(t.Hacker), Venue=tostring(t.Venue), Type=tostring(t.Type)
```

### Enable Continious Export of ADX DBase (Tables) to ADLSv2 (LT storage) via managed identities (system)
Microsoft Source Document: [here!](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/management/data-export/continuous-export-with-managed-identity?tabs=system-assigned%2Cazure-storage)
![image](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/26a304ac-d73c-49e9-ad69-1317a152e96c)

### Acquire schema from an ADX internal table to create an external table via ADLSv2
![AF95AC0F-3E1A-4EE8-A470-1FD5D8685FD3_1_201_a](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/133e808a-cb4e-4bda-85c4-f35645bdbb75)


