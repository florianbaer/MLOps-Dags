import pickle


def train(params: dict):
    from modules.tasks.credentials import setup_credentials
    from modules.tasks.gcs import download_from_gcs, upload_to_gcs
    from airflow.models import Variable
    import os
    import logging
    import pandas as pd
    import wandb
    from sklearn.decomposition import PCA

    logger = logging.getLogger(__name__)
    setup_credentials()

    # W&B setup
    os.environ['WANDB_API_KEY'] = Variable.get('AIRFLOW_VAR_WANDB_TOKEN')
    wandb.login(key=os.environ['WANDB_API_KEY'])
    run = wandb.init(
        project="swiss-ai-jobs", entity="florianbaer",
        job_type="training", name=f"training_{params['date_str']}"
    )

    # Download preprocessed data
    date_str = params['date_str']
    download_from_gcs(f"dataset/{date_str}.parquet", "export.parquet")
    df = pd.read_parquet("export.parquet")

    # Log dataset artifact
    artifact = wandb.Artifact('dataset', type='dataset')
    artifact.add_file('export.parquet')
    run.log_artifact(artifact)

    # Train PCA
    components = 2
    run.log({'n_rows': len(df), 'components': components, 'date': date_str})
    pca = PCA(n_components=components)
    logger.info(f"Start PCA with {components} components")
    df['pca'] = pca.fit_transform(df['description_embedding'].tolist()).tolist()

    # Save and upload model
    with open('pca.pickle', 'wb') as f:
        pickle.dump(pca, f)
    upload_to_gcs('pca.pickle', f"models/pca_{date_str}.pickle")

    # Log model artifact
    artifact = wandb.Artifact('pca', type='model')
    artifact.add_file('pca.pickle')
    run.log_artifact(artifact)
    run.finish()
