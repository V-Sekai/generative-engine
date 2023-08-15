defmodule GenerativeSidecarApi do
  @base_url "http://127.0.0.1:8000/"
  @headers [{"Content-Type", "application/json"}]

  def run_tests do
    list_objects()
    get_3d_conventions()
    import_obj("/Users/ernest.lee/Downloads/untitled_rem_p0_10_quadrangulation.obj")
    delete_obj("untitled_rem_p0_10_quadrangulation")
    list_objects()
    batch_request()
    batch_mesh()
    create_empty_mesh("mesh_name", "object_name")
    set_translation("object_name1", [2, 0, 0])
    set_parent("object_name2", "object_name1")
    set_global_transform("mesh_name0","object_name1", [[1,0,0], [0,1,0], [0,0,1], [0,0,0]])
    export_gltf("New_Object", "C:/Users/ernes/Desktop/generative_sidecar/file.gltf")
    import_gltf("C:/Users/ernes/Desktop/generative_sidecar/file.gltf")
  end

  def batch_mesh do
    add_vertices("object_name1","mesh_name0", [[1,0,0], [2,0,0], [2,1,0], [1,1,0], [1,0,1], [2,0,1], [2,1,1], [1,1,1]])
    add_faces("object_name1", "mesh_name0",[[0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7], [0,1,2,3], [4,5,6,7]])
  end

  def list_objects do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "list_objects", "id" => 1})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def get_3d_conventions do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "get_3d_conventions", "id" => 1})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def import_obj(path) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "import_obj", "params" => [path], "id" => 2})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def delete_obj(name) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "delete_obj", "params" => [name], "id" => 3})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def batch_request do
    body = Jason.encode!([
      %{"jsonrpc" => "2.0", "method" => "list_objects", "id" => 1},
      %{"jsonrpc" => "2.0", "method" => "import_obj", "params" => ["C:\\Users\\ernes\\Desktop\\generative_engine\\untitled_rem_p0_10_quadrangulation.obj"], "id" => 2},
      %{"jsonrpc" => "2.0", "method" => "delete_obj", "params" => ["untitled_rem_p0_10_quadrangulation"], "id" => 3},
      %{"jsonrpc" => "2.0", "method" => "list_objects", "id" => 4}
    ])
    HTTPoison.put!(@base_url, body, @headers)
  end

  def create_empty_mesh(mesh_name, object_name) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "create_empty_mesh", "params" => [mesh_name, object_name], "id" => 1})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def add_vertices(object_name, mesh_name, vertices) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "add_vertices", "params" => [object_name, mesh_name, vertices], "id" => 1})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def add_faces(object_name, mesh_name, faces) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "add_faces", "params" => [object_name, mesh_name, faces], "id" => 2})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def set_translation(object_name, translation) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "set_translation", "params" => [object_name, translation], "id" => 3})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def set_parent(child_object_name, parent_object_name) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "set_parent", "params" => [child_object_name, parent_object_name], "id" => 4})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def set_global_transform(mesh_name, object_name, transform) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "set_global_transform", "params" => [mesh_name, object_name, transform], "id" => 5})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def export_gltf(object_name, file_path) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "export_gltf", "params" => [object_name, file_path], "id" => 6})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def import_gltf(file_path) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => "import_gltf", "params" => [file_path], "id" => 7})
    HTTPoison.put!(@base_url, body, @headers)
  end
end
