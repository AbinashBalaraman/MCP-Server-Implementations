from mcp.server.fastmcp import FastMCP




mcp = FastMCP('test1')

@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two integers"""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="stdio")

# @mcp.tool()
# def mongodb(query : dict):
   
#     """use mpognodb query for access data in collection.
#     Args:
#         the query will be used in  result = myCollection.find(query)
#         query (str): JSON string for query or text search
#         Returns:Result of the database operation
#         sends the query to the MongoDB collection and returns the result."""
#     result = myCollection.find(query)
#     return result