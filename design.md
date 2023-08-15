# GLTF Scene Decomposition API

This API provides a set of operations for decomposing a GLTF scene into standalone components. It includes methods for importing and exporting GLTF files, setting parent-child relationships between objects, creating empty meshes, adding vertices and faces to meshes, setting object translations, rotations, and scales, and copying materials, skeletons, and animations from one object to another.

Handle three.js, Godot Engine and Blender.

## Suggested New API Operations

- `copy_materials(source_object: str, target_object: str) -> str`
  - Copies all materials from the source object to the target object.
  
- `copy_skeleton(source_object: str, target_object: str) -> str`
  - Copies the skeleton (if any) from the source object to the target object.
  
- `copy_animations(source_object: str, target_object: str) -> str`
  - Copies all animations from the source object to the target object.
  
- `copy_object(source_object: str, target_object: str) -> str`
  - Copies all properties and data (including materials, skeleton, and animations) from the source object to the target object. It uses all the above functions internally.

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