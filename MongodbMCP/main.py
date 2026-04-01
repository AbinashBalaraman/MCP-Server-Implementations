from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient
import requests
from pymongo.errors import InvalidOperation

client = MongoClient("mongodb://localhost:27017/")
current_db = client["car"]  # Default db
current_collection = current_db["car_data"]  # Default collection

mcp = FastMCP('Mongo')

@mcp.tool()
def add_two_numbers(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

@mcp.tool()
def list_databases() -> list:
    """List all database names on the server."""
    return client.list_database_names()

@mcp.tool()
def list_collections(db_name: str) -> list:
    """List all collections in the given database."""
    db = client[db_name]
    return db.list_collection_names()

@mcp.tool()
def set_database(db_name: str):
    """Change the default database being used."""
    global current_db, current_collection
    current_db = client[db_name]
    # Optionally reset collection to None or default
    current_collection = None
    return f"Current database set to {db_name}"

@mcp.tool()
def set_collection(coll_name: str):
    """Set the default collection in the current database."""
    global current_collection
    current_collection = current_db[coll_name]
    return f"Current collection set to {coll_name} in db {current_db.name}"

@mcp.tool()
def collection_operations(action: str, query: dict, document: dict, update: dict, limit: int):
    """Handle all collection-level operations (CRUD).
    check query format of mongo db skip extra atributes if the dont necessary"""
    if current_collection is None:
        return "No collection is set. Please set a collection with set_collection()."
    try:
        if action == "find":
            cursor = current_collection.find(query or {})
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        elif action == "insert":
            if document:
                result = current_collection.insert_one(document)
                return "added successfully with id: " + str(result.inserted_id)
            else:
                return "Document required"
        elif action == "update":
            if query and update:
                result = current_collection.update_many(query, update)
                return 'updated successfully with count: ' + str(result.modified_count)
            else:
                return "Query and update required"
        elif action == "delete":
            if query:
                result = current_collection.delete_many(query)
                return "deleted successfully with count: " + str(result.deleted_count)
            else:
                return "Query required"
        elif action == "count":
            return current_collection.count_documents(query or {})
        elif action == "distinct":
            if query and "field" in query:
                field = query["field"]
                filter_query = query.get("filter", {})
                return current_collection.distinct(field, filter_query)
            else:
                return "Field name required in query"
        else:
            return f"Unknown action: {action}"
    except Exception as e:
        return str(e)

@mcp.tool()
def tavily(params: dict):
    """Get data from Tavily API."""
    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.prompt()
def prompt_for_tavily(a):
    """Prompt for Tavily search parameters"""
    return """Performs a web search using the Tavily API...
    (rest of prompt unchanged)
    """



prompj = """
You are an API agent handling MongoDB collection operations... 
"""

@mcp.prompt()
def mongodbprompt(q):
    return prompj

if __name__ == "__main__":
    mcp.run(transport="stdio")