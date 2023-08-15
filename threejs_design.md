Here's a design suggestion for launching a website with Three.js using Elixir and Phoenix. This will allow you to mirror the API.

First, create a new Phoenix project:

```elixir
mix phx.new generative_sidecar_web --no-ecto
```

Then, in your `router.ex`, define a route that will serve your HTML page:

```elixir
defmodule GenerativeSidecarWeb.Router do
  use GenerativeSidecarWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  scope "/", GenerativeSidecarWeb do
    pipe_through :browser

    get "/", PageController, :index
  end
end
```

Create a `PageController` with an index action:

```elixir
defmodule GenerativeSidecarWeb.PageController do
  use GenerativeSidecarWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
```

In your `page/index.html.eex`, include the Three.js library and write your JavaScript code:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Generative Sidecar</title>
    <script src="https://threejs.org/build/three.js"></script>
  </head>
  <body>
    <div id="container"></div>
    <script>
      // Your Three.js code goes here
    </script>
  </body>
</html>
```

Finally, in your `GenerativeSidecarApi` module, add functions to handle AJAX requests from your Three.js code. These functions should call the appropriate functions in your existing `GenerativeSidecarApi` module:

```elixir
defmodule GenerativeSidecarWeb.GenerativeSidecarApiController do
  use GenerativeSidecarWeb, :controller

  def list_objects(conn, _params) do
    objects = GenerativeSidecarApi.list_objects()
    json(conn, %{objects: objects})
  end

  # Add similar functions for other API methods
end
```

And add routes for these functions in your `router.ex`:

```elixir
scope "/api", GenerativeSidecarWeb do
  pipe_through :api

  get "/list_objects", GenerativeSidecarApiController, :list_objects
  # Add similar routes for other API methods
end
```

This way, your Three.js code can make AJAX requests to these routes to interact with your API.