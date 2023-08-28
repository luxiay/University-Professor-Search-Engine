
import pymongo as mdb
import pandas as pd

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'academicworld'

class MongoConnector:
    def __init__(self):
        client = mdb.MongoClient(MONGODB_HOST, MONGODB_PORT)
        self.db = client[DB_NAME]

    # widget 2: Top publication
    def GetPublicationsInfo(self):
        query = [
            {"$project": {"_id": 0, "title": 1}},
            {"$sort": {"num_citations": -1}},
            {"$limit": 10}
        ]
        # Execute the aggregation pipeline
        data = self.db.publications.aggregate(query)
        df = pd.DataFrame(data)

        return df

    # widget 6: Faculty Information Search
    def QueryFacultyTable(self, university_name, faculty_name):
        query = [
            {
                "$match": {
                    "name": faculty_name,
                    "affiliation.name": university_name
                }
            },
            {
                "$project": {
                    "name": 1,
                    "position": 1,
                    "university": "$affiliation.name",
                    "email": 1,
                    "phone": 1,
                    "photoUrl": 1
                }
            }
        ]

        result = list(self.db.faculty.aggregate(query))
        df = pd.DataFrame(result)

        return df
