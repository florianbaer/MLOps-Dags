from google.cloud import firestore


class FirestoreService:

    def __init__(self, project_name, collection_name, database_name):
        self.collection_name = collection_name
        self.db = firestore.Client(project=project_name, database=database_name)

    def get_all(self):
        return self.db.collection(self.collection_name).get()

    def get_by_id(self, document_id):
        return self.db.collection(self.collection_name).document(document_id).get()

    def create(self, id, data):
        doc = self.db.collection(self.collection_name).document(id)
        return doc.set(data)

    def create_multiple(self, data):
        batch = self.db.batch()
        for item in data:
            ref = self.db.collection(self.collection_name).document()
            batch.set(ref, item)
        return batch

    def update(self, document_id, data):
        return self.db.collection(self.collection_name).document(document_id).update(data)

    def delete(self, document_id):
        return self.db.collection(self.collection_name).document(document_id).delete()

class AsyncFirestoreService:
    def __init__(self, project_name, collection_name, database_name):
        self.collection_name = collection_name
        self.db = firestore.AsyncClient(project=project_name, database=database_name)

    async def get_all(self):
        return self.db.collection(self.collection_name).get()

    async def get_by_id(self, document_id):
        return await self.db.collection(self.collection_name).document(document_id).get()

    async def create(self, id, data):
        doc = self.db.collection(self.collection_name).document(id)
        return await doc.create(data)

    async def get_existing_ids(self):
        docs = await self.db.collection(self.collection_name).select(['id']).get()
        return [doc.id for doc in docs]

    async def create_multiple(self, data):
        batch = self.db.batch()
        for id, item in data:
            ref = self.db.collection(self.collection_name).document(id)
            batch.set(ref, item)
        return batch.commit()

    async def update(self, document_id, data):
        return await self.db.collection(self.collection_name).document(document_id).update(data)

    async def delete(self, document_id):
        return await self.db.collection(self.collection_name).document(document_id).delete()

    async def close(self):
        return self.db.close()

