import requests
from couchbase.cluster import Cluster
from couchbase.auth import PasswordAuthenticator

class Admin():
    def __init__(self):
        self.data = []
    def createBucket(self, uid, pwd, host, bucket, drop=False, ramquota=256, db_port=8091):
        if drop:
            print('Dropping Bucket')        
            self.dropBucket(uid, pwd, host, bucket)
        data = {
        'name': bucket,
        'ramQuotaMB': ramquota,
        'flushEnabled' : 1
        }
        url='http://' + host + ':' + str(db_port) + '/pools/default/buckets/'
        print(url)
        response = requests.post(url, data=data, auth=(uid, pwd))
        print(response)

    def createScope(self, uid, pwd, host, bucket, scope, db_port=8091):
        data = {
        'name': scope
        }
        url='http://' + host + ':' + str(db_port) +'/pools/default/buckets/' + bucket + '/scopes'
        print(url)
        response = requests.post(url, data=data, auth=(uid, pwd))
        print(response)

    def createScope(self, uid, pwd, host, bucket, scope, db_port=8091):
        url='http://' + host + ':' + str(db_port) +'/pools/default/buckets/' + bucket + '/scopes/' + scope
        print(url)
        response = requests.delete(url, auth=(uid, pwd))
        print(response)

    def createCollection(self, uid, pwd, host, bucket, scope, collection, db_port=8091):
        data = {
        'name': collection,
        'maxTTL': 0
        }
        url='http://' + host + ':' + str(db_port) +'/pools/default/buckets/' + bucket + '/scopes/' + scope + "/collections"
        print(url)
        response = requests.post(url, data=data, auth=(uid, pwd))
        print(response)

    def dropCollection(self, uid, pwd, host, bucket, scope, collection, db_port=8091):
        url='http://' + host + ':' + str(db_port) +'/pools/default/buckets/' + bucket + '/scopes/' + scope + "/collections/" + collection
        print(url)
        response = requests.delete(url, auth=(uid, pwd))
        print(response)

    def dropBucket(self, uid, pwd, host, bucket, db_port=8091):
        url='http://' + host + ':' + str(db_port) +'/pools/default/buckets/' + bucket
        response = requests.delete(url, auth=(uid, pwd))
        print(response)

class Ops():
    def __init__(self,  host, uid, pwd, bucket, scope='_default', collection='_default'):
        import couchbase 
        from couchbase.cluster import Cluster, ClusterOptions
        from couchbase_core.cluster import PasswordAuthenticator
        from couchbase.cluster import QueryOptions
        print(bucket)
        self.cluster = Cluster('couchbase://' + host, ClusterOptions(
        PasswordAuthenticator(uid, pwd)))
        self.cb = self.cluster.bucket(bucket)
        self.collection = self.cb.collection(collection)
        self.data = []
    def add(self, id, document):
        result = self.collection.insert(id, document)
        return result
    def get(self, id):
        result = self.collection.insert(id)
        return result
    def delete(self, id, document):
        result = self.collection.delete(id)
        return result
    def update(self, id, document):
        result = self.collection.upsert(id, document)
        return result
    def runQuery(self, query):
        return self.cluster.query(query).execute()
