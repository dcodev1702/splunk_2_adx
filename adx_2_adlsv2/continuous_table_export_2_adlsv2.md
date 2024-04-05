Ensure the identity used has sufficent access/permissions to the ADX Cluster.
* On the cluster, go to the "permissions" blade, select "AllDatabasesAdmin" and add your identity. <br />
[Set permissions on ADX Cluster](https://learn.microsoft.com/en-us/azure/data-explorer/manage-cluster-permissions)

![image](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/b055961d-a65d-483a-b331-627605469ed5)



[Setup continious export from ADX DBase Table to ADLSv2 (external table)](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/management/data-export/continuous-export-with-managed-identity?tabs=system-assigned%2Cazure-storage)
```console
.alter-merge cluster policy managed_identity ```[
    {
      "ObjectId": "system",
      "AllowedUsages": "AutomatedFlows"
    }
]```
```
System Assigned Identity: 9dd3e9c8-b114-xxxx-xxx-xxxxxxxxxxxx
![4C5FD731-5FE9-48BE-8CB1-30844C88EC7D_1_201_a](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/afad8dd2-2a26-4525-94f2-ba7e20729bd6)

Give the System Assigned Identity access to the database (requires admin access rights)
```console
.add database ['sentinel-2-adx'] admins ('aadapp=9dd3e9c8-b114-xxxx-xxx-xxxxxxxxxxxx')
```

[Create ADLSv2 Storage Account (SA)](https://learn.microsoft.com/en-us/azure/storage/blobs/create-data-lake-storage-account) and container where data of the external table will reside. <br />
Assign System Assigned Identity to the newly created ADLSv2 Storage Account: [ADX -> Identity -> Add 'Storage Blob Data Contributor']
![6A7DBF0A-8301-4D3E-A33C-F52CF0BAFD7D](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/c0c82abd-aa8d-432d-9b4f-e9b55902b835)

Create the external table in ADLSv2 container: <br />
Storage Account/Container: "https://dodealogretention.blob.core.windows.net/hearbeat/m2131/data;impersonate" <br />
Table Schema's from internal table [ADX] has to exactly match the external table [ADLSv2] you're creating. <br />
Existing internal table schema can then be copied and directly applied to create the external table. <br />
```console
.show table Heartbeat cslschema | project Schema
```
![FF1EA34C-B7F1-4BA0-AD09-5FB8956D3A99](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/40767554-60b7-407c-b422-d5c4544682c2)

Supported Data Formats: CSV, JSON, and PARQUET <br />
<span style="color:blue">*!!!! THE EXTERNAL TABLE SCHEMA HAS TO MATCH THE INTERNAL TABLE SCHEMA !!!!*</span>

```console
.create external table HeartbeatEXT (TenantId:string,SourceSystem:string,TimeGenerated:datetime,MG:string,ManagementGroupName:string,SourceComputerId:string,ComputerIP:string,Computer:string,Category:string,OSType:string,OSName:string,OSMajorVersion:string,OSMinorVersion:string,Version:string,SCAgentChannel:string,IsGatewayInstalled:string,RemoteIPLongitude:string,RemoteIPLatitude:string,RemoteIPCountry:string,SubscriptionId:string,ResourceGroup:string,ResourceProvider:string,Resource:string,ResourceId:string,ResourceType:string,ComputerEnvironment:string,Solutions:string,VMUUID:string,ComputerPrivateIPs:string,Type:string,_ResourceId:string)
kind=storage
dataformat=parquet 
( 
    h@'https://dodealogretention.blob.core.windows.net/heartbeat/m2131/data;impersonate' 
)
```

Create a continious export job from ADX [Heartbeat] -> ADLSv2 [HeartbeatEXT]
```console
.create-or-alter continuous-export HeartbeatExport over (Heartbeat) to table HeartbeatEXT with (managedIdentity="system", intervalBetweenRuns=5m) <| Heartbeat
```
![9BF8A98F-9B55-4C5E-B7F1-750D38DDD89D](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/509903bb-bc8a-4065-ab40-01f225d9da98)


ADX QUERY (internal table) <br />
The internal and external tables should operate in the same manner with respect to KQL queries <br />
```console
Heartbeat

Heartbeat
| where Computer == 'MIR8-Win10-ADM.student7.local' and TimeGenerated > ago(10m)
```

ADLSv2 QUERY (external table) <br />
```console
external_table("HeartbeatEXT")

external_table('HeartbeatEXT')
| where Computer == 'MIR8-Win10-ADM.student7.local' and TimeGenerated > ago(10m)
```
![AF95AC0F-3E1A-4EE8-A470-1FD5D8685FD3_1_201_a](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/133e808a-cb4e-4bda-85c4-f35645bdbb75)
