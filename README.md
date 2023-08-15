# README

# Request to list_objects from Blender
curl -X PUT http://127.0.0.1:8000/ \
-H 'Content-Type: application/json' \
-d '{"jsonrpc": "2.0", "method": "list_objects", "id": 1}'

# Request to list_objects from Blender
curl -X PUT http://127.0.0.1:8000/ \
-H 'Content-Type: application/json' \
-d '{"jsonrpc": "2.0", "method": "get_3d_conventions", "id": 1}'

# Request to import_obj from Blender
curl -X PUT http://127.0.0.1:8000/ \
-H 'Content-Type: application/json' \
-d '{"jsonrpc": "2.0", "method": "import_obj", "params": ["/Users/ernest.lee/Downloads/untitled_rem_p0_10_quadrangulation.obj"], "id": 2}'

# Request to delete_obj from Blender
curl -X PUT http://127.0.0.1:8000/ \
-H 'Content-Type: application/json' \
-d '{"jsonrpc": "2.0", "method": "delete_obj", "params": ["untitled_rem_p0_10_quadrangulation"], "id": 3}'

# Another request to list_objects from Blender
curl -X PUT http://127.0.0.1:8000/ \
-H 'Content-Type: application/json' \
-d '{"jsonrpc": "2.0", "method": "list_objects", "id": 4}'

# Batch request to list_objects, import_obj, delete_obj and list_objects again from Blender
curl -X PUT http://127.0.0.1:8000/ \
-H 'Content-Type: application/json' \
-d '[
  {"jsonrpc": "2.0", "method": "list_objects", "id": 1},
  {"jsonrpc": "2.0", "method": "import_obj", "params": ["C:\Users\ernes\Desktop\generative_engine\untitled_rem_p0_10_quadrangulation.obj"], "id": 2},
  {"jsonrpc": "2.0", "method": "delete_obj", "params": ["untitled_rem_p0_10_quadrangulation"], "id": 3},
  {"jsonrpc": "2.0", "method": "list_objects", "id": 4}
]'

# Create empty mesh
curl -X PUT \
-H "Content-Type: application/json" \
-d '[{"jsonrpc": "2.0", "method": "create_empty_mesh", "params": ["mesh_name", "object_name"], "id": 1}]' \
http://127.0.0.1:8000

# Shape 1
curl -X PUT \
-H "Content-Type: application/json" \
-d '[ 
    {"jsonrpc": "2.0", "method": "add_vertices", "params": ["object_name1","mesh_name0",  [[1,0,0], [2,0,0], [2,1,0], [1,1,0], [1,0,1], [2,0,1], [2,1,1], [1,1,1]]], "id": 1}, 
    {"jsonrpc": "2.0", "method": "add_faces", "params": ["object_name1", "mesh_name0",[[0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7], [0,1,2,3], [4,5,6,7]]], "id": 2} 
]' \
http://127.0.0.1:8000

# Shape 2
curl -X PUT \
-H "Content-Type: application/json" \
-d '[ 
    {"jsonrpc": "2.0", "method": "add_vertices", "params": ["object_name2", "mesh_name1",[[1,0,0], [2,0,0], [2,1,0], [1,1,0], [1,0,1], [2,0,1], [2,1,1], [1,1,1]]], "id": 3}, 
    {"jsonrpc": "2.0", "method": "add_faces", "params": ["object_name2", "mesh_name1",[[0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7], [0,1,2,3], [4,5,6,7]]], "id": 4} 
]' \
http://127.0.0.1:8000

# Shape 3
curl -X PUT \
-H "Content-Type: application/json" \
-d '[ 
    {"jsonrpc": "2.0", "method": "add_vertices", "params": ["object_name3", "mesh_name2",[[1,0,0], [2,0,0], [2,1,0], [1,1,0], [1,0,1], [2,0,1], [2,1,1], [1,1,1]]], "id": 5}, 
    {"jsonrpc": "2.0", "method": "add_faces", "params": ["object_name3", "mesh_name2",[[0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7], [0,1,2,3], [4,5,6,7]]], "id": 6} 
]' \
http://127.0.0.1:8000

# Set translation for Shape 1
curl -X PUT \
-H "Content-Type: application/json" \
-d '[ 
    {"jsonrpc": "2.0", "method": "set_translation", "params": ["object_name1", [2, 0, 0]], "id": 7}
]' \
http://127.0.0.1:8000

# Set translation for Shape 2
curl -X PUT \
-H "Content-Type: application/json" \
-d '[ 
    {"jsonrpc": "2.0", "method": "set_translation", "params": ["object_name2", [4, 0, 0]], "id": 8}
]' \
http://127.0.0.1:8000

# Set translation for Shape 3
curl -X PUT \
-H "Content-Type: application/json" \
-d '[ 
    {"jsonrpc": "2.0", "method": "set_translation", "params": ["object_name3", [6, 0, 0]], "id": 9}
]' \
http://127.0.0.1:8000

# Set parent for Shape 2
curl -X PUT \
-H "Content-Type: application/json" \
-d '[ 
    {"jsonrpc": "2.0", "method": "set_parent", "params": ["object_name2", "object_name1"], "id": 11}
]' \
http://127.0.0.1:8000

# Set parent for Shape 3
curl -X PUT \
-H "Content-Type: application/json" \
-d '[ 
    {"jsonrpc": "2.0", "method": "set_parent", "params": ["object_name3", "object_name2"], "id": 12}
]' \
http://127.0.0.1:8000

# Set Global Transform
curl -X PUT \
-H "Content-Type: application/json" \
-d '[ 
    {"jsonrpc": "2.0", "method": "set_global_transform", "params": ["mesh_name0","object_name1", [[1,0,0], [0,1,0], [0,0,1], [0,0,0]]], "id": 8} 
]' \
http://127.0.0.1:8000

# Request to export_gltf from Blender
curl -X PUT http://127.0.0.1:8000/ -H 'Content-Type: application/json' -d '{"jsonrpc": "2.0", "method": "export_gltf", "params": ["New_Object", "C:/Users/ernes/Desktop/generative_engine/file.gltf"], "id": 6}'

# Request to import_gltf from Blender
curl -X PUT http://127.0.0.1:8000/ \
-H 'Content-Type: application/json' \
-d '{"jsonrpc": "2.0", "method": "import_gltf", "params": ["C:/Users/ernes/Desktop/generative_engine/file.gltf"], "id": 5}'
