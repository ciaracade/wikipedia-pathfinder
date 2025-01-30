import os
import subprocess
from neo4j import GraphDatabase

# Configuration
CSV_FILENAME = "wikipedia_links_2025-01-29.csv"
LOCAL_CSV_PATH = f"data/csv/{CSV_FILENAME}"
NEO4J_IMPORT_PATH = f"/var/lib/neo4j/import/{CSV_FILENAME}"
CSV_URL = f"file://{NEO4J_IMPORT_PATH}"

# Neo4j connection settings
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

def is_neo4j_running_in_docker():
    """Check if Neo4j is running inside a Docker container."""
    try:
        result = subprocess.run(["docker", "ps", "--filter", "name=neo4j", "--format", "{{.Names}}"], capture_output=True, text=True)
        return "neo4j" in result.stdout.strip()
    except FileNotFoundError:
        return False  # Docker is not installed

def copy_csv_to_neo4j():
    """Automatically copy CSV to Neo4j's import directory (inside Docker or locally)."""
    if is_neo4j_running_in_docker():
        print("🚀 Neo4j is running inside Docker. Copying CSV to container...")
        subprocess.run(["docker", "cp", LOCAL_CSV_PATH, f"neo4j:{NEO4J_IMPORT_PATH}"], check=True)
        subprocess.run(["docker", "exec", "neo4j", "chown", "neo4j:neo4j", NEO4J_IMPORT_PATH], check=True)
    else:
        print("🚀 Neo4j is running locally. Ensuring import directory exists...")
        os.makedirs("/var/lib/neo4j/import", exist_ok=True)
        subprocess.run(["mv", LOCAL_CSV_PATH, NEO4J_IMPORT_PATH], check=True)

def import_csv_to_neo4j():
    """Import Wikipedia links CSV into Neo4j."""
    print(f"✅ Latest CSV file: {CSV_FILENAME}")

    # Copy CSV to Neo4j before import
    copy_csv_to_neo4j()

    # Connect to Neo4j
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{CSV_URL}' AS row
        MERGE (a:Article {{title: row.source}})
        MERGE (b:Article {{title: row.target}})
        MERGE (a)-[:LINKS_TO]->(b);
        """
        session.run(query)
        print(f"✅ Successfully imported {CSV_FILENAME} into Neo4j!")

if __name__ == "__main__":
    import_csv_to_neo4j()
