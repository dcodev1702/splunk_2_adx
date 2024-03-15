
from datetime import timedelta
import ast

from azure.kusto.data import KustoClient, KustoConnectionStringBuilder, ClientRequestProperties
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table

def main():

    '''
    1. Create App Registration & Secret from Entra ID
    2. Record Client_ID, Client_Secret, and Tenant_ID from App Registration
    3. Create Database
    4. Within the Database -- Assign Admin permission to App Registration
    5. Create Table within ADX Database
    .create table record (Timestamp:datetime, Trace:dynamic)

    6. Populate the record table with test data
    .ingest inline into table record [2024-03-15,"{""Company"":""MFCC-G9-DOG"", ""Hacker"":""JJ Bottles"", ""Venue"":""ShmooCon""}"]
    .ingest inline into table record [2024-03-15,"{""Company"":""TrustedSec"", ""Hacker"":""Carlos Perez"", ""Venue"":""BSides PR""}"]
    .ingest inline into table record [2024-03-15,"{""Company"":""TrustedSec"", ""Hacker"":""Edwin David"", ""Venue"":""BSides NoVA""}"]
    '''
    
    ######################################################
    ##                        AUTH                      ##
    ######################################################

    # Note that the 'help' cluster only allows interactive
    # access by AAD users (and *not* AAD applications)
    ADX_CLUSTER      = "https://<clust_name>.<location>.kusto.windows.net"
    CLIENT_ID        = "ENTER_YOUR_CLIENT_ID"
    CLIENT_SECRET    = "ENTER_YOUR_CLIENT_SECRET"
    AAD_TENANT_ID    = "ENTER_YOUR_TENANT_ID"
    KUSTO_INGEST_URI = "https://ingest-<cluster_name>.<location>.kusto.windows.net/"
    KUSTO_DATABASE   = "splunk-2-adx"

    # Authenticate to ADX Cluster / DBase using Entra ID App Registration (client id & client secret)
    kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(CLUSTER, CLIENT_ID, CLIENT_SECRET, AAD_TENANT_ID)
    
    # The authentication method will be taken from the chosen KustoConnectionStringBuilder.
    with KustoClient(kcsb) as kusto_client:
        query = "record"
        response = kusto_client.execute(KUSTO_DATABASE, query)
      
        print("ADX Hacker Stats:")
        idx = 0
        for key, value in response.primary_results[0]:
            # Print each record and their values
            print(f"Timestamp: {key} :: RECORD-{idx} :: Company: {value['Company']}, Hacker: {value['Hacker']}, Venue: {value['Venue']}")
            idx += 1
          
        kusto_client.close()


if __name__ == "__main__":
    main()
