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

HOST = "127.0.0.1"
PORT = 8000

def export_gltf(obj_name, gltf_path):
    # Check if the object exists in the scene.
    if obj_name not in bpy.data.objects:
        return f"Object {obj_name} does not exist"

    # Schedule the export operation to be run in the main thread
    bpy.app.timers.register(functools.partial(_export_gltf_main_thread, obj_name, gltf_path))

    return "OK"

def _export_gltf_main_thread(obj_name, gltf_path):
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

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.handle_request()

    def do_PUT(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        request = json.loads(data)
        self.handle_request(request)

    def shutdown(self):
        self.server.shutdown()


    def handle_request(self, request=None):
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

    def handle_single_request(self, request):
        method = request.get('method')  # Get method from request body
        params = request.get('params', [])
        id = request.get('id')

        if method == 'list_objects':
            result = self.list_objects(*params)
            response = self.success_response(result, id)
        elif method == 'import_obj':
            result = self.import_obj(*params)
            response = self.success_response(result, id)
        elif method == 'import_gltf':
            result = self.import_gltf(*params)
            response = self.success_response(result, id)
        elif method == 'export_gltf':
            result = export_gltf(*params)
            response = self.success_response(result, id)
        elif method == 'get_3d_conventions':
            result = self.get_3d_conventions(*params)
            response = self.success_response(result, id)
        elif method == 'delete_obj':
            result = self.delete_obj(*params)
            response = self.success_response(result, id)
        elif method == 'create_mesh_from_vertices':
            result = self.create_mesh_from_vertices(*params)
            response = self.success_response(result, id) 
        elif method == 'shutdown':
            self.shutdown()
            response = self.success_response("Server is shutting down", id)
        else:
            response = self.error_response(-32601, f"Method not found: {method}", id)

        return response

    def import_gltf(self, gltf_path):
        import os

        if not os.path.isfile(gltf_path):
            return f"File {gltf_path} does not exist"

        # Try to import the .gltf file.
        try:
            bpy.ops.import_scene.gltf(filepath=gltf_path)
        except Exception as e:
            return f"Failed to import {gltf_path}: {e}"

        return "OK"


    def create_mesh_from_vertices(self, vertex_list):
        # Create a new mesh object and link it to the scene
        mesh = bpy.data.meshes.new(name="New_Mesh")
        obj = bpy.data.objects.new("New_Object", mesh)
        bpy.context.collection.objects.link(obj)

        # Create a bmesh object and add vertices to it
        bm = bmesh.new()
        for v in vertex_list:
            coords = (v['x'], v['y'], v['z'])  # Extract coordinates from the dictionary
            bm.verts.new(coords)  # Add a new vertex

        # Update the bmesh to the mesh
        bm.to_mesh(mesh)
        bm.free()

        return "Mesh created from vertices"

    def success_response(self, result, id):
        return {
            "result": result,
            "id": id
        }

    def error_response(self, code, message, id):
        return {
            "error": {
                "code": code,
                "message": message
            },
            "id": id
        }

    def list_objects(self):
        return bpy.data.objects.keys()
                
    def get_3d_conventions(self):
        # Get the current 3D view space conventions
        view3d_space = next(space for space in bpy.context.screen.areas if space.type == 'VIEW_3D').spaces[0]
        view_rotation = view3d_space.region_3d.view_rotation

        return {
            "view_rotation": tuple(view_rotation)
        }

    def delete_obj(self, obj_name):
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

    def import_obj(self, node_path):
        import os

        if node_path in bpy.data.objects:
            return f"Object {obj_name} already exists"

        # Try to import the .obj file.
        try:
            bpy.ops.import_scene.obj(filepath=node_path)
        except Exception as e:
            return f"Failed to import {node_path}: {e}"

        return "OK"

def launch_server():
    server = HTTPServer((HOST, PORT), RequestHandler)
    server.serve_forever()

def server_start():
    try:
        print("Starting server...")
        t = threading.Thread(target=launch_server)
        t.daemon = True
        t.start()
        print("Server started successfully.")
    except Exception as e:
        print(f"Failed to start server: {e}")

server_start()