defmodule GenerativeSidecarApi do
  @base_url "http://127.0.0.1:8000/"
  @headers [{"Content-Type", "application/json"}]

  def run_tests do
    Enum.each([:list_objects, :get_3d_conventions, {:import_obj, "/Users/ernest.lee/Downloads/untitled_rem_p0_10_quadrangulation.obj"},
               {:delete_obj, "untitled_rem_p0_10_quadrangulation"}, :list_objects, :batch_request, :batch_mesh,
               {:create_empty_mesh, ["mesh_name", "object_name"]}, {:set_translation, ["object_name1", [2, 0, 0]]},
               {:set_parent, ["object_name2", "object_name1"]}, {:set_global_transform, ["mesh_name0","object_name1", [[1,0,0], [0,1,0], [0,0,1], [0,0,0]]]},
               {:export_gltf, ["New_Object", "C:/Users/ernes/Desktop/generative_sidecar/file.gltf"]}, {:import_gltf, "C:/Users/ernes/Desktop/generative_sidecar/file.gltf"}],
              &apply(__MODULE__, &1))
  end

  defp make_request(method, params \\ [], id \\ 1) do
    body = Jason.encode!(%{"jsonrpc" => "2.0", "method" => method, "params" => params, "id" => id})
    HTTPoison.put!(@base_url, body, @headers)
  end

  def list_objects, do: make_request("list_objects")
  def get_3d_conventions, do: make_request("get_3d_conventions")
  def import_obj(path), do: make_request("import_obj", [path])
  def delete_obj(name), do: make_request("delete_obj", [name])
  def batch_request, do: make_request("batch_request")
  def create_empty_mesh(mesh_name, object_name), do: make_request("create_empty_mesh", [mesh_name, object_name])
  def add_vertices(object_name, mesh_name, vertices), do: make_request("add_vertices", [object_name, mesh_name, vertices])
  def add_faces(object_name, mesh_name, faces), do: make_request("add_faces", [object_name, mesh_name, faces])
  def set_translation(object_name, translation), do: make_request("set_translation", [object_name, translation])
  def set_parent(child_object_name, parent_object_name), do: make_request("set_parent", [child_object_name, parent_object_name])
  def set_global_transform(mesh_name, object_name, transform), do: make_request("set_global_transform", [mesh_name, object_name, transform])
  def export_gltf(object_name, file_path), do: make_request("export_gltf", [object_name, file_path])
  def import_gltf(file_path), do: make_request("import_gltf", [file_path])

  def batch_mesh do
    object_name = "object_name1"
    mesh_name = "mesh_name0"
    add_vertices(object_name, mesh_name, [[1,0,0], [2,0,0], [2,1,0], [1,1,0], [1,0,1], [2,0,1], [2,1,1], [1,1,1]])
    add_faces(object_name, mesh_name,[[0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7], [0,1,2,3], [4,5,6,7]])
  end
end
