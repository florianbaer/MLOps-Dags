def download_and_upload_to_volume(params: dict):
    from modules.tasks.credentials import setup_credentials
    from modules.tasks.gcs import download_from_gcs
    import os
    import modal

    setup_credentials()

    date_str = params['date_str']
    path_filename = os.path.abspath("pca.pickle")

    # Download model from GCS
    download_from_gcs(f"models/pca_{date_str}.pickle", path_filename)

    # Upload to Modal volume
    volume = modal.Volume.from_name(date_str, create_if_missing=True)
    if volume.listdir('/'):
        volume.remove_file("pca.pickle")
    with volume.batch_upload() as upload:
        upload.put_file(path_filename, "pca.pickle")

    os.remove(path_filename)
