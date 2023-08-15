# Copyright (c) 2018-present. This file is part of V-Sekai https://v-sekai.org/.
# SaracenOne & K. S. Ernest (Fire) Lee & Lyuma & MMMaellon & Contributors
# blender_xml_rpc.py
# SPDX-License-Identifier: MIT

from http.server import BaseHTTPRequestHandler, HTTPServer
import bpy
import threading
import json
import urllib.parse as urlparse
import bmesh
import functools 
from typing import List, Tuple, Union, Optional, Dict, Any

HOST = "127.0.0.1"
PORT = 8000

def set_parent(child_name: str, parent_name: str) -> str:
    if child_name in bpy.data.objects and parent_name in bpy.data.objects:
        bpy.app.timers.register(functools.partial(_set_parent_main_thread, child_name, parent_name))
        return f"Set {parent_name} as parent of {child_name}"
    else:
        return "Child or Parent object does not exist"

def _set_parent_main_thread(child_name: str, parent_name: str) -> None:
    # Check if the child and parent objects exist in the scene.
    if child_name not in bpy.data.objects or parent_name not in bpy.data.objects:
        print(f"Child or Parent object does not exist")
        return

    try:
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Get the child and parent objects
        child = bpy.data.objects[child_name]
        parent = bpy.data.objects[parent_name]

        # Select the child object and make it the active object
        child.select_set(True)
        bpy.context.view_layer.objects.active = child

        # Select the parent object
        parent.select_set(True)

        # Set the parent of the active object
        override = {'selected_objects': [child, parent], 'active_object': child, 'object': child}
        bpy.ops.object.parent_set(override, type='OBJECT')

        print(f"Set {parent_name} as parent of {child_name}")
    except Exception as e:
        print(f"Failed to set {parent_name} as parent of {child_name}: {e}")

def export_gltf(obj_name: str, gltf_path: str) -> str:
    # Check if the object exists in the scene.
    if obj_name not in bpy.data.objects:
        return f"Object {obj_name} does not exist"

    # Schedule the export operation to be run in the main thread
    bpy.app.timers.register(functools.partial(_export_gltf_main_thread, obj_name, gltf_path))

    return "OK"

def _export_gltf_main_thread(obj_name: str, gltf_path: str) -> None:
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select the object
    obj = bpy.data.objects[obj_name]
    obj.select_set(True)

    # Set the active object
    bpy.context.view_layer.objects.active = obj

    # Try to export the object to a .gltf file.
    try:
        # Check if there is an active object
        if bpy.context.view_layer.objects.active is not None:
            # Override the context
            override = {'selected_objects': [obj], 'active_object': obj, 'object': obj}
            bpy.ops.export_scene.gltf(override, filepath=gltf_path)
        else:
            print(f"No active object to export")
    except Exception as e:
        print(f"Failed to export {obj_name} to {gltf_path}: {e}")

class BatchMeshOperations:
    def __init__(self, object_name: str):
        if object_name in bpy.data.objects:
            self.obj = bpy.data.objects[object_name]
        else:
            # Create a new object if it doesn't exist
            mesh = bpy.data.meshes.new(object_name)
            self.obj = bpy.data.objects.new(object_name, mesh)
            bpy.context.collection.objects.link(self.obj)

        self.mesh = self.obj.data
        self.bm = bmesh.new()
        self.bm.from_mesh(self.mesh)

    def create_empty_mesh(self, mesh_name: str, object_name: str) -> str:
        self.mesh = bpy.data.meshes.new(mesh_name)
        self.obj = bpy.data.objects.new(object_name, self.mesh)
        bpy.context.collection.objects.link(self.obj)
        return self.obj.name

    def add_vertices(self, object_name: str, mesh_name: str, vertices: List[Tuple[float, float, float]]) -> str:
        self.__init__(object_name)
        for x, y, z in vertices:
            self.bm.verts.new((x, y, z))
        self.bm.to_mesh(self.mesh)
        return "Vertices added"

    def add_faces(self, object_name: str, mesh_name: str, faces: List[List[int]]) -> str:
        self.__init__(object_name)
        self.bm.verts.ensure_lookup_table()  # Update the internal index table
        for vertices in faces:
            if all(isinstance(i, int) for i in vertices):
                self.bm.faces.new([self.bm.verts[i] for i in vertices])
            else:
                raise ValueError("All elements in 'vertices' should be integers.")
        self.bm.to_mesh(self.mesh)
        return "Faces added"

    def set_translation(self, object_name: str, translation: Tuple[float, float, float]) -> str:
        if object_name in bpy.data.objects:
            obj = bpy.data.objects[object_name]
            obj.location = translation
            return f"Translation set for {object_name}"
        else:
            return f"Object {object_name} does not exist"

    def set_rotation(self, object_name: str, rotation: Tuple[float, float, float]) -> str:
        if object_name in bpy.data.objects:
            obj = bpy.data.objects[object_name]
            obj.rotation_euler = rotation
            return f"Rotation set for {object_name}"
        else:
            return f"Object {object_name} does not exist"

    def set_scale(self, object_name: str, scale: Tuple[float, float, float]) -> str:
        if object_name in bpy.data.objects:
            obj = bpy.data.objects[object_name]
            obj.scale = scale
            return f"Scale set for {object_name}"
        else:
            return f"Object {object_name} does not exist"

    def find_edges(self, edges: List[Tuple[int, int]]) -> str:
        found_edges = []
        for v1, v2 in edges:
            edge = self.bm.edges.get((self.bm.verts[v1], self.bm.verts[v2]))
            if edge:
                found_edges.append(edge)
        return f"Edges found: {found_edges}"

    def remove_edges(self, edges: List[int]) -> str:
        for edge in edges:
            self.bm.edges.remove(self.bm.edges[edge])
        return "Edges removed"

    def neighbor_faces(self, vertices: List[int]) -> str:
        all_faces = []
        for vertex in vertices:
            faces = [f.index for f in self.bm.verts[vertex].link_faces]
            all_faces.extend(faces)
        return f"Neighbor faces: {all_faces}"

    def loops(self, face_vertex_pairs: List[Tuple[int, int]]) -> str:
        found_loops = []
        for face, vertex in face_vertex_pairs:
            loop = next((l for l in self.bm.faces[face].loops if l.vert == self.bm.verts[vertex]), None)
            if loop:
                found_loops.append(loop)
        return f"Loops found: {found_loops}"

    def add_vertex_attributes(self, attribute_definitions: List[str]) -> str:
        for attribute_definition in attribute_definitions:
            self.bm.verts.layers.float.new(attribute_definition)
        return f"Vertex attributes '{attribute_definitions}' added"

    def add_edge_attributes(self, attribute_definitions: List[str]) -> str:
        for attribute_definition in attribute_definitions:
            self.bm.edges.layers.float.new(attribute_definition)
        return f"Edge attributes '{attribute_definitions}' added"

    def add_face_attributes(self, attribute_definitions: List[str]) -> str:
        for attribute_definition in attribute_definitions:
            self.bm.faces.layers.float.new(attribute_definition)
        return f"Face attributes '{attribute_definitions}' added"

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self) -> None:
        self.handle_request()

    def do_PUT(self) -> None:
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        request = json.loads(data)
        self.handle_request(request)

    def shutdown(self) -> None:
        self.server.shutdown()


    def handle_request(self, request: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None) -> None:
        try:
            if isinstance(request, list):  # Check if the request is a batch
                responses = []
                for req in request:
                    response = self.handle_single_request(req)
                    if response:  # Don't include responses for notifications
                        responses.append(response)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(json.dumps(responses), 'utf8'))
            else:  # If not a batch, handle as a single request
                response = self.handle_single_request(request)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(json.dumps(response), 'utf8'))
        except Exception as e:
            response = {
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                },
                "id": None
            }
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf8'))


    def handle_single_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get('method')  # Get method from request body
        params = request.get('params', [])
        id = request.get('id')

        object_name = None
        batch_ops = None
        if params:
            # Assuming the first parameter is always the object name
            object_name = params[0]
            batch_ops = BatchMeshOperations(object_name)
        method_mapping = {
            'list_objects': lambda params: self.list_objects(*params),
            'import_obj': lambda params: self.import_obj(*params),
            'import_gltf': lambda params: self.import_gltf(*params),
            'export_gltf': lambda params: export_gltf(*params),
            'get_3d_conventions': lambda params: self.get_3d_conventions(*params),
            'delete_obj': lambda params: self.delete_obj(*params),
            'set_parent': lambda params: set_parent(*params) if len(params) >= 2 else self.error_response("Insufficient parameters for 'set_parent'"),
            'set_translation': lambda params: batch_ops.set_translation(*params) if len(params) >= 2 else self.error_response("Insufficient parameters for 'set_translation'"),
            'set_rotation': lambda params: batch_ops.set_rotation(*params) if len(params) >= 2 else self.error_response("Insufficient parameters for 'set_rotation'"),
            'set_scale': lambda params: batch_ops.set_scale(*params) if len(params) >= 2 else self.error_response("Insufficient parameters for 'set_scale'"),
            'create_empty_mesh': lambda params: batch_ops.create_empty_mesh(*params) if len(params) >= 2 else self.error_response("Insufficient parameters for 'create_empty_mesh'"),
            'add_vertices': lambda params: batch_ops.add_vertices(*params) if len(params) >= 3 else self.error_response("Insufficient parameters for 'add_vertices'"),
            'add_faces': lambda params: batch_ops.add_faces(*params) if len(params) >= 3 else self.error_response("Insufficient parameters for 'add_faces'"),
            'find_edges': lambda params: batch_ops.find_edges(params[1:]),
            'remove_edges': lambda params: batch_ops.remove_edges(params[1:]),
            'neighbor_faces': lambda params: batch_ops.neighbor_faces(params[1:]),
            'loops': lambda params: batch_ops.loops(params[1:]),
            'add_vertex_attributes': lambda params: batch_ops.add_vertex_attributes(params[1:]),
            'add_edge_attributes': lambda params: batch_ops.add_edge_attributes(params[1:]),
            'add_face_attributes': lambda params: batch_ops.add_face_attributes(params[1:]),
            'run_tests': lambda params: self.run_tests(*params),
            'shutdown': lambda params: self.shutdown()
        }

        if method in method_mapping:
            result = method_mapping[method](params)
            response = self.success_response(result, id)
        else:
            response = self.error_response(-32601, f"Method not found: {method}", id)

        return response

    def import_gltf(self, gltf_path: str) -> str:
        import os

        if not os.path.isfile(gltf_path):
            return f"File {gltf_path} does not exist"

        # Try to import the .gltf file.
        try:
            bpy.ops.import_scene.gltf(filepath=gltf_path)
        except Exception as e:
            return f"Failed to import {gltf_path}: {e}"

        return "OK"


    def success_response(self, result: Any, id: Optional[int]) -> Dict[str, Any]:
        return {
            "result": result,
            "id": id
        }

    def error_response(self, code: int, message: str, id: Optional[int]) -> Dict[str, Any]:
        return {
            "error": {
                "code": code,
                "message": message
            },
            "id": id
        }

    def list_objects(self) -> List[str]:
        return bpy.data.objects.keys()
                
    def get_3d_conventions(self) -> Dict[str, Tuple[float, float, float, float]]:
        # Get the current 3D view space conventions
        view3d_space = next(space for space in bpy.context.screen.areas if space.type == 'VIEW_3D').spaces[0]
        view_rotation = view3d_space.region_3d.view_rotation

        return {
            "view_rotation": tuple(view_rotation)
        }

    def delete_obj(self, obj_name: str) -> str:
        # Check if the object exists in the scene.
        if obj_name in bpy.data.objects:
            # Get the object.
            obj = bpy.data.objects[obj_name]

            # Unlink the object from all scenes (this effectively deletes it).
            bpy.data.objects.remove(obj)

            return f"Object {obj_name} deleted"
        else:
            # If the object does not exist, return a message indicating so.
            return f"Object {obj_name} does not exist"

    def import_obj(self, node_path: str) -> str:
        import os

        if node_path in bpy.data.objects:
            return f"Object {obj_name} already exists"

        # Try to import the .obj file.
        try:
            bpy.ops.import_scene.obj(filepath=node_path)
        except Exception as e:
            return f"Failed to import {node_path}: {e}"

        return "OK"

def launch_server() -> None:
    server = HTTPServer((HOST, PORT), RequestHandler)
    server.serve_forever()

def server_start() -> None:
    try:
        print("Starting server...")
        t = threading.Thread(target=launch_server)
        t.daemon = True
        t.start()
        print("Server started successfully.")
    except Exception as e:
        print(f"Failed to start server: {e}")

server_start()
