def preprocessing(params: dict):
    from modules.tasks.credentials import setup_credentials
    from modules.tasks.gcs import download_from_gcs, upload_to_gcs
    import pandas as pd
    from bs4 import BeautifulSoup
    import spacy

    setup_credentials()

    date_str = params['date_str']
    download_from_gcs(f"export/{date_str}.parquet", "export.parquet")
    df = pd.read_parquet("export.parquet")

    df['description_text'] = df['description_html'].apply(
        lambda html: BeautifulSoup(html, 'html.parser').get_text()
    )

    nlp = spacy.load("en_core_web_sm")
    df['description_embedding'] = [doc.vector for doc in nlp.pipe(df['description_text'], batch_size=32)]

    df.to_parquet("export_cleaned.parquet")
    upload_to_gcs("export_cleaned.parquet", f"dataset/{date_str}.parquet")
