import neo4j
from neo4j import GraphDatabase
import pandas as pd

# URI = "bolt://localhost:7687"
# USERNAME = "neo4j"
# PASSWORD = "12345678"

class Neo4jConnector:
  def __init__(self):
    self.URI = "bolt://localhost:7687"
    #self.AUTH = ("neo4j", "password@12345678")
    self.AUTH = ("neo4j", "qiu19900612")

  # widget 1： Top N kewords
  def widgetOne(self, num):
      driver = GraphDatabase.driver(self.URI, auth=self.AUTH)
      with driver.session(database="academicworld") as session:
        record = session.execute_read(self.helper, num=num)
      df = pd.DataFrame(record)
      session.close()
      driver.close()
      df.rename(columns={0: 'top words', 1: 'count'}, inplace=True)
      return df

  @staticmethod
  def helper(tx, num):
    query = "MATCH (p:PUBLICATION)-[r:LABEL_BY]->(k:KEYWORD) WITH k.name as keyword, count(*) as count ORDER BY count DESC RETURN keyword, toInteger(count) as count LIMIT $num"

    result = tx.run(query, num=num)
    output = list(result)
    return output
