import modal

date_str = "DATE_STR"


image = modal.Image.debian_slim().pip_install("fastapi[standard]").pip_install('spacy').pip_install('https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl').pip_install('scikit-learn')

#date_str = '2024_12_03_13_19_15'
volume = modal.Volume.from_name(date_str, create_if_missing=True)
app = modal.App(name="embedding",image=image, volumes={"/data": volume})

@app.function()
@modal.web_endpoint()
def get_embedding(text: str='Hello World'):
    import spacy
    import pickle
    nlp = spacy.load("en_core_web_sm")
    pca = pickle.load(open("/data/pca.pickle", "rb"))
    res = pca.transform([nlp(text).vector])[0].tolist()
    return res, date_str
