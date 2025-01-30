from neo4j import GraphDatabase
import os

# Neo4j connection settings
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def test_neo4j():
    """Test connection to Neo4j by running a simple query."""
    try:
        with driver.session() as session:
            result = session.run("RETURN 'Neo4j Connected!' AS message")
            print(result.single()["message"])  # Should print: Neo4j Connected!
        return True
    except Exception as e:
        print(f"Neo4j connection failed: {e}")
        return False

# Run the test
if __name__ == "__main__":
    if test_neo4j():
        print("✅ Neo4j connection successful!")
    else:
        print("❌ Failed to connect to Neo4j.")
