import urllib.request
​
key = "blahblahblah"
​
h = urllib.request.urlopen("https://sg5ef35168.execute-api.us-east-1.amazonaws.com/dev")
​
h.add_header("Key", key)
​
h.get()
