from urllib.parse import urlencode, urljoin

def construct_url(base_url, query_params):

    base_url = "https://api.trademe.co.nz/v1/Search/Motors/Used.json"

    # Encode the query parameters
    query_string = urlencode(query_params)
    
    # Construct the full URL
    full_url = urljoin(base_url, '?' + query_string)
    
    return full_url


# # Example Usage

# # Dictionary of query parameters
# query_params = {
#     "sort_order": "ExpiryDesc",
#     "page": "1",
#     "rows": "500"
# }

# # Construct the URL
# full_url = construct_url(base_url, query_params)

# print(full_url)
