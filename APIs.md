info:
  title: Competition Graph API

paths:
  /api/comp/dow30:
    get:
      description: Returns information about Dow 30 companies.
      responses:
        '200':
          description: A JSON array containing Dow 30 company information.
          content:
            application/json:

  /api/comp/sp500:
    get:
      description: Returns information about S&P 500 companies.
      responses:
        '200':
          description: A JSON array containing S&P 500 company information.
          content:
            application/json:

  /api/comp/sample:
    get:
      description: Returns sample data for testing purposes.
      responses:
        '200':
          description: A JSON object containing sample data.
          content:
            application/json:

  /api/comp/surrounding:
    get:
      description: Returns surrounding nodes with optional filtering parameters.
      parameters:
        - in: query
          name: node_id
          description: The ID of the node to retrieve surrounding nodes for.
          required: true
          schema:
            type: integer
        - in: query
          name: expand_number_of_layers
          description: The number of layers to expand the search for surrounding nodes.
          required: true
          schema:
            type: integer
        - in: query
          name: competition
          description: Filter by competition category.
          schema:
            type: boolean
            default: true
        - in: query
          name: other
          description: Filter by other category.
          schema:
            type: boolean
            default: false
        - in: query
          name: product
          description: Filter by product category.
          schema:
            type: boolean
            default: true
        - in: query
          name: unknown
          description: Filter by unknown category.
          schema:
            type: boolean
            default: false
      responses:
        '200':
          description: A JSON object containing filtered surrounding nodes.
          content:
            application/json:

response:
    schema:
        links: json
        nodes: json
    example:
        { "links": [ { "category": "competition", "source": "175", "target": "178" }, { "category": "competition", "source": "175", "target": "179" } ], "nodes": [ { "id": "175", "name": "NKE" }, { "id": "178", "name": "SYNC.1" }, { "id": "179", "name": "VFC" } ] }