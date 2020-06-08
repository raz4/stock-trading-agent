from google.cloud import storage


def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    
    bucket_name, destination_location = _parse_gcs_uri(destination_blob_name)

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_location)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_location
        )
    )

def download_blob(source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    bucket_name, source_location = _parse_gcs_uri(source_blob_name)

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_location)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_location, destination_file_name
        )
    )

def _parse_gcs_uri(uri):
    """
    Parse a GCS file uri to get bucket name and file path
    :param uri: GCS file uri
    :return: tuple with bucket name, file path
    """
    splitted = uri.split("gs://")[-1].split('/')
    bucket_name = splitted[0]
    file_path = '/'.join(splitted[1:])
    
    return bucket_name, file_path
