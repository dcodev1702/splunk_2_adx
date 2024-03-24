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
```console
.add database ['sentinel-2-adx'] admins ('aadapp=9dd3e9c8-xxxx-4311-xxx-xxxxxxxxxxxx')
```

Create ADLSv2 storage account and Container where data for the external table will reside. <br />
Assign Managed Identity to ADLSv2 Container [ADX -> Identity -> Add 'Storage Blob Data Contributor']

Create table in ADLSv2 container: <br />
Storage Account: "https://adxlogretention.blob.core.windows.net/hearbeatext/m2131/data;impersonate" <br />
Table Schema's from internal table has to exactly match the external table you're creating
Existing internal table schema can be copied and directly applied to create the external table
Example:
```console
.show table Heartbeat cslschema
```
![BD918AE0-1407-4091-8EC7-A65CF26A75CC](https://github.com/dcodev1702/splunk_2_adx/assets/32214072/4f9484fc-3c4d-4ef2-b55e-d1bfae328b4e)

Supported Data Formats: CSV, JSON, and PARQUET <br />
<span style="color:blue">*!!!! THE EXTERNAL TABLE SCHEMA HAS TO MATCH THE INTERNAL TABLE SCHEMA !!!!*</span>

```console
.create external table HeartbeatEXT (TenantId:string,SourceSystem:string,TimeGenerated:datetime,MG:string,ManagementGroupName:string,SourceComputerId:string,ComputerIP:string,Computer:string,Category:string,OSType:string,OSName:string,OSMajorVersion:string,OSMinorVersion:string,Version:string,SCAgentChannel:string,IsGatewayInstalled:string,RemoteIPLongitude:string,RemoteIPLatitude:string,RemoteIPCountry:string,SubscriptionId:string,ResourceGroup:string,ResourceProvider:string,Resource:string,ResourceId:string,ResourceType:string,ComputerEnvironment:string,Solutions:string,VMUUID:string,ComputerPrivateIPs:string,Type:string,_ResourceId:string) kind=storage dataformat=parquet 
( 
    h@'https://adxlogretention.blob.core.windows.net/heartbeatext/m2131/data;impersonate' 
)
```

Create a continious export job from ADX -> ADLSv2
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
