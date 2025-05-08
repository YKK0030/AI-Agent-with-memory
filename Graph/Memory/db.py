import json
import time
from types import SimpleNamespace

class Neo4jMemoryStore:
    def __init__(self, kg_client):
        self.kg = kg_client

    def put_memory(self, namespace: tuple, key: str, value: dict):
        ns = "|".join(namespace)
        now = int(time.time())
        cypher = """
        MERGE (m:Memory {namespace: $ns, key: $key})
        SET m.value = $val, m.timestamp = $ts
        """
        self.kg.query(
            cypher,
            params={
                "ns": ns,
                "key": key,
                "val": json.dumps(value),  # ← JSON string so Neo4j sees a primitive
                "ts": now,
            },
        )

    def search_memory(self, namespace: tuple, limit: int = 5):
        ns = "|".join(namespace)
        cypher = """
        MATCH (m:Memory {namespace: $ns})
        RETURN m.key AS key, m.value AS value
        ORDER BY m.timestamp DESC
        LIMIT $limit
        """
        records = self.kg.query(cypher, params={"ns": ns, "limit": limit})
        results = []
        for record in records:
            val = json.loads(record["value"])   # ← parse back to dict
            results.append(SimpleNamespace(key=record["key"], value=val))
        return results