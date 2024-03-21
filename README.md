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
8. Install Python 3.X w/ the Kusto Python SDK (Windows / Linux / MacOS)
   ```console
      mkdir .adx_python
      python -m venv adx_demo
      source adx_demo/bin/activate
   ```
   ```console
      pip install azure-kusto-data
      pip install azure-kusto-ingest
   ```
   
## Illustration
### Ingestion: Python Kusto SDK used to programmatically authenicate & ingest data [data_ingest_all.json]
![image](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/757a1101-0645-487f-a4ec-b6c39d797935)

### ADX Database Query (SplunkTable) via Python Kusto SDK
![image](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/40b61863-2b81-4e0b-add7-22881bb7473d)

### ADX Database Query (SplunkTable) via ADX
![image](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/812b5597-70cd-4363-a5d4-0e4d07cbee0e)

### Enable Continious Export of ADX DBase (Tables) to ADLSv2 (LT storage) via managed identities (system)
![image](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/26a304ac-d73c-49e9-ad69-1317a152e96c)

