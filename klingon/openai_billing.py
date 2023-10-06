import requests

def get_openai_billing_info(api_key, start_date, end_date):
    """
    Retrieve billing information from OpenAI API.
    
    Parameters:
        api_key (str): The API key for authenticating with OpenAI.
        start_date (str): The start date for the billing period in YYYY-MM-DD format.
        end_date (str): The end date for the billing period in YYYY-MM-DD format.
    
    Returns:
        dict: The JSON response from the API containing billing information.
    """
    # Define the API endpoint and parameters
    url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Make the API call
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful and return the JSON response
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to retrieve data. Status code: {response.status_code}"}

# Sample usage:
# Uncomment to test the function
# api_key = "your_openai_api_key_here"
# start_date = "2023-05-01"
# end_date = "2023-05-31"
# billing_info = get_openai_billing_info(api_key, start_date, end_date)
# print(billing_info)
