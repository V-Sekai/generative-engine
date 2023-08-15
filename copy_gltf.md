# GLTF Scene Decomposition API

This API provides a set of operations for decomposing a GLTF scene into standalone components. It includes methods for importing and exporting GLTF files, setting parent-child relationships between objects, creating empty meshes, adding vertices and faces to meshes, setting object translations, rotations, and scales, and copying materials, skeletons, and animations from one object to another.

## Existing API Operations

- `import_gltf(gltf_path: str) -> str`
  - Imports a GLTF file from the specified path.
  
- `export_gltf(obj_name: str, gltf_path: str) -> str`
  - Exports a GLTF file to the specified path.
  
- `set_parent(child_name: str, parent_name: str) -> str`
  - Sets the parent-child relationship between two objects.
  
- `create_empty_mesh(mesh_name: str, object_name: str) -> str`
  - Creates an empty mesh with the given name and associates it with the specified object.
  
- `add_vertices(object_name: str, mesh_name: str, vertices: List[Tuple[float, float, float]]) -> str`
  - Adds vertices to the specified mesh of the given object.
  
- `add_faces(object_name: str, mesh_name: str, faces: List[List[int]]) -> str`
  - Adds faces to the specified mesh of the given object.
  
- `set_translation(object_name: str, translation: Tuple[float, float, float]) -> str`
  - Sets the translation of the specified object.
  
- `set_rotation(object_name: str, rotation: Tuple[float, float, float]) -> str`
  - Sets the rotation of the specified object.
  
- `set_scale(object_name: str, scale: Tuple[float, float, float]) -> str`
  - Sets the scale of the specified object.

## Suggested New API Operations

- `copy_materials(source_object: str, target_object: str) -> str`
  - Copies all materials from the source object to the target object.
  
- `copy_skeleton(source_object: str, target_object: str) -> str`
  - Copies the skeleton (if any) from the source object to the target object.
  
- `copy_animations(source_object: str, target_object: str) -> str`
  - Copies all animations from the source object to the target object.
  
- `copy_object(source_object: str, target_object: str) -> str`
  - Copies all properties and data (including materials, skeleton, and animations) from the source object to the target object. It uses all the above functions internally.

## Additional API Operations

- `add_vertex_attributes(object_name: str, attributes: Dict[str, List[Tuple[float, float, float]]]) -> str`
  - Adds vertex attributes to the specified object. The attributes parameter is a dictionary where the key is the attribute name (e.g., "uv_map", "bones") and the value is a list of tuples representing the attribute values.

- `get_object_properties(object_name: str) -> Dict[str, Any]`
  - Returns a dictionary containing all properties of the specified object.

- `set_object_properties(object_name: str, properties: Dict[str, Any]) -> str`
  - Sets the properties of the specified object based on the provided dictionary.

- `create_light_source(light_type: str, light_properties: Dict[str, Any]) -> str`
  - Creates a new light source in the scene with the specified type and properties.

- `create_camera(camera_type: str, camera_properties: Dict[str, Any]) -> str`
  - Creates a new camera in the scene with the specified type and properties.

- `create_texture(texture_path: str) -> str`
  - Imports a texture from the specified path and returns its name.

- `apply_texture(object_name: str, texture_name: str) -> str`
  - Applies the specified texture to the given object.