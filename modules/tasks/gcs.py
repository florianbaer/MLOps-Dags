BUCKET_NAME = 'hslu-swiss-ai-jobs'


def upload_to_gcs(local_path, remote_path, bucket_name=BUCKET_NAME):
    from google.cloud import storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_path, if_generation_match=0)


def download_from_gcs(remote_path, local_path, bucket_name=BUCKET_NAME):
    from google.cloud import storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(remote_path)
    blob.download_to_filename(local_path)
