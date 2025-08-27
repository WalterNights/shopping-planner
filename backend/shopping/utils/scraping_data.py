HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"}

GRAPHQL_URL = "https://www.exito.com/api/graphql"

QUERY = """
    query SearchQuery(
        $first: Int!, 
        $after: String, 
        $sort: StoreSort!, 
        $term: String!, 
        $selectedFacets: [SelectedFacetInput!]!
    ) {
      productSearch(
        first: $first
        after: $after
        sort: $sort
        term: $term
        selectedFacets: $selectedFacets
      ) {
        products {
          productId
          productName
          brand
          linkText
          items {
            itemId
            images {
              imageUrl
            }
            sellers {
              commertialOffer {
                Price
              }
            }
          }
        }
        recordsFiltered
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
"""