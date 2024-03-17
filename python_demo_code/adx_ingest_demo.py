from time import sleep
from azure.kusto.data import KustoConnectionStringBuilder
from azure.kusto.data.helpers import dataframe_from_result_table
from azure.kusto.data.data_format import DataFormat
from azure.kusto.ingest import (
    ReportLevel,
    FileDescriptor,
    IngestionProperties,
    IngestionMappingKind,
    QueuedIngestClient,
)

# https://learn.microsoft.com/en-us/azure/data-explorer/ingest-json-formats?tabs=python
def main():

    ######################################################
    ##                        AUTH                      ##
    ######################################################
    # Note that the 'help' cluster only allows interactive
    # access by AAD users (and *not* AAD applications)
    ADX_CLUSTER       = "https://<cluster>.<location>.kusto.windows.net"
    CLIENT_ID         = ""
    CLIENT_SECRET     = ""
    AAD_TENANT_ID     = ""
    KUSTO_INGEST_URI  = "https://ingest-<cluster>.<location>.kusto.windows.net/"
    KUSTO_DATABASE    = "splunk-2-adx"
    KUSTO_DBASE_TABLE = "SplunkTableRaw"

kcsb_ingest = KustoConnectionStringBuilder.with_aad_application_key_authentication(KUSTO_INGEST_URI, CLIENT_ID, CLIENT_SECRET, AAD_TENANT_ID)

    # The authentication method will be taken from the chosen KustoConnectionStringBuilder.
    with QueuedIngestClient(kcsb_ingest) as kusto_client:
        
        ingestion_props = IngestionProperties(
            database=KUSTO_DATABASE, 
            table=KUSTO_DBASE_TABLE,
            flush_immediately=True,
            data_format=DataFormat.MULTIJSON, #USE FOR JSON ARRAYS
            #data_format=DataFormat.JSON,       #USE FOR SINGLE JSON OBJECTS
            report_level=ReportLevel.FailuresAndSuccesses,
            ingestion_mapping_kind=IngestionMappingKind.JSON,
            ingestion_mapping_reference="SplunkTableMapping"
        )

        '''
        # ingest from json files with a single JSON object per line
        for i in range(6):
            file_descriptor = FileDescriptor(f"./logs/data_ingest-{i}.json")  # 4096 is the raw size of the data in bytes.
            result = kusto_client.ingest_from_file(file_descriptor, ingestion_properties=ingestion_props)
            
            # Inspect the result for useful information, such as source_id and blob_url
            print(repr(result))
            sleep(1)
        '''

        file_descriptor = FileDescriptor(f"./logs/data_ingest_all.json")
        result = kusto_client.ingest_from_file(file_descriptor, ingestion_properties=ingestion_props)
        
        print(repr(result))
        kusto_client.close()
        

if __name__ == "__main__":
    main()
