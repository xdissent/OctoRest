from octorest import OctoRest, WorkflowAppKeyRequestResult

def main():
    url = "http://octopi.local"
    user = "user"
    
    client = None

    try:
        client = OctoRest(url=url)
    except TypeError:
        raise NotImplementedError() # Decide what should happen now

    (result, api_key) = (None, None)

    try:
        (result, api_key) = client.try_get_api_key('my-app', user)
    except ConnectionError:
        raise NotImplementedError() # Decide what should happen now. Suggestion - tell the user the OctoPrint server is unreachable and that he should check the URL entered

    if result == WorkflowAppKeyRequestResult.WORKFLOW_UNSUPPORTED:
        raise NotImplementedError() # Decide what should happen now. Suggestion - fall back to asking the user to manually enter a valid API key.
    elif result == WorkflowAppKeyRequestResult.TIMED_OUT: # The user took too long to approve the API key request
        raise NotImplementedError() # Decide what should happen now
    elif result == WorkflowAppKeyRequestResult.NOPE: # The request has been denied
        raise NotImplementedError() # Decide what should happen now
    elif result == WorkflowAppKeyRequestResult.GRANTED:
        client.load_api_key(api_key) # You have to load the API key before sending any requests to the OctoPrint server
        pass # At this point you can use the client for whatever you wish
    
    raise NotImplementedError() # Decide what should happen now

if __name__ == "__main__":
    main()