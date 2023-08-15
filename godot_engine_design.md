For Godot Engine 4.0, you can use GDScript to make HTTP requests to your Elixir API. Here's a basic example of how you might set this up.

Firstly, in Godot, create a new script (let's call it `Api.gd`) and add the following code:

```gdscript
extends Node

var http_request = HTTPRequest.new()

func _ready():
    self.add_child(http_request)
    http_request.connect("request_completed", self, "_on_request_completed")

func list_objects():
    var error = http_request.request("http://localhost:4000/api/list_objects")
    if error != OK:
        print("An error occurred: ", error)

func _on_request_completed(result, response_code, headers, body):
    var json = JSON.parse(body.get_string_from_utf8())
    print(json.result) # prints the result of the API call
```

In this script, we're creating an `HTTPRequest` node, which we can use to make HTTP requests. We're also defining a `list_objects` function that makes a GET request to the `/api/list_objects` endpoint of our Elixir API.

The `_on_request_completed` function is a callback that gets called when the HTTP request is completed. It parses the JSON response from the API and prints the result.

You can call the `list_objects` function from another script like so:

```gdscript
extends Node

onready var api = preload("res://Api.gd").new()

func _ready():
    api.list_objects()
```

This will make a request to the API when the node is ready and print the result.

Remember to replace `"http://localhost:4000/api/list_objects"` with the actual URL of your Elixir API. Also, ensure that your Elixir server is running and accessible from Godot.

Please note that Godot Engine 4.0 is still in development at the time of writing, and some features may change or be unavailable.