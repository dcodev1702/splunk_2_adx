
from datetime import timedelta
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder, ClientRequestProperties
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table

def main():

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

    kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(ADX_CLUSTER, CLIENT_ID, CLIENT_SECRET, AAD_TENANT_ID)

    # The authentication method will be taken from the chosen KustoConnectionStringBuilder.
    with KustoClient(kcsb) as kusto_client:
        
        # QUERY ADX DBASE TABLE
        query = "SplunkTable \
                | extend p = parse_json(FWLogEntry) \
                | sort by todatetime(p.TimeGenerated) desc \
                | distinct TimeGenerated=todatetime(p.TimeGenerated), Company=tostring(p.Company), Hacker=tostring(p.Hacker), Venue=tostring(p.Venue), Type=tostring(p.Type)"

        response = kusto_client.execute(KUSTO_DATABASE, query)

        print("ADX Hacker Stats:")
        idx = 0
        for record in response.primary_results[0]:
            # Print the desired keys and their values
            print(f"RECORD={idx} -> Timestamp: {record['TimeGenerated']} - Company: {record['Company']} - Hacker: {record['Hacker']} - Venue: {record['Venue']} - Type: {record['Type']}")
            idx += 1

        kusto_client.close()

if __name__ == "__main__":
    main()
