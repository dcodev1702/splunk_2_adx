from datetime import timedelta

from azure.kusto.data import KustoClient, KustoConnectionStringBuilder, ClientRequestProperties
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
from azure.kusto.data.data_format import DataFormat, IngestionMappingKind
from azure.kusto.ingest import (
    BlobDescriptor,
    FileDescriptor,
    IngestionProperties,
    ReportLevel,
    IngestionStatus,
    KustoStreamingIngestClient,
    ManagedStreamingIngestClient,
    QueuedIngestClient,
    StreamDescriptor,
)

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
    KUSTO_DBASE_TABLE = "SplunkTable"

    kcsb_ingest = KustoConnectionStringBuilder.with_aad_application_key_authentication(KUSTO_INGEST_URI, CLIENT_ID, CLIENT_SECRET, AAD_TENANT_ID)

    # The authentication method will be taken from the chosen KustoConnectionStringBuilder.
    with QueuedIngestClient(kcsb_ingest) as kusto_client:
        
        ingestion_props = IngestionProperties(
            database=KUSTO_DATABASE, 
            table=KUSTO_DBASE_TABLE,
            flush_immediately=True,
            data_format=DataFormat.JSON,
            report_level=ReportLevel.FailuresAndSuccesses,
            #ingestion_mapping_kind=IngestionMappingKind.JSON,
            #ingestion_mapping_reference="SplunkTable_JSON_Mapping",
        )

        # ingest from json file: splunk_ingest_demo.json
        file_descriptor = FileDescriptor("./splunk_ingest_demo.json", 4000)  # 4000 is the raw size of the data in bytes.
        kusto_client.ingest_from_file(file_descriptor, ingestion_properties=ingestion_props)
        result = kusto_client.ingest_from_file("./splunk_ingest_demo.json", ingestion_properties=ingestion_props)

        # Inspect the result for useful information, such as source_id and blob_url
        print(repr(result))
        kusto_client.close()
        

if __name__ == "__main__":
    main()
