from python_graphql_client import GraphqlClient

# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="http://10.0.0.124:7070/graphql")

def get_pwd(username: str)->str:

    # Create the query string and variables required for the request.
    query = """
        query ($data: PersonInput!) {
            persons(data:$data) {
                name,
                username,
                pwd
            }
        }
    """
    variables = {"data": {"username":str(username)}}

    # Synchronous request
    data = client.execute(query=query, variables=variables)
    return data

