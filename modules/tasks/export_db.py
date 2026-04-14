def db_export(params: dict):
    from modules.tasks.credentials import setup_credentials
    from modules.tasks.gcs import upload_to_gcs
    from google.cloud import firestore
    import pandas as pd
    import logging

    setup_credentials()
    logger = logging.getLogger(__name__)

    date_str = params['date_str']
    db = firestore.Client(project="sage-mind-371111", database="swiss-ai-jobs")

    objects = [doc.to_dict() for doc in db.collection('swiss-ai-jobs').stream()]
    df = pd.DataFrame(objects)
    logger.info(f"Exported {len(objects)} documents from Firestore")

    df.to_parquet("export.parquet")
    upload_to_gcs("export.parquet", f"export/{date_str}.parquet")
