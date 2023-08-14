# Copyright (c) 2018-present. This file is part of V-Sekai https://v-sekai.org/.
# SaracenOne & K. S. Ernest (Fire) Lee & Lyuma & MMMaellon & Contributors
# blender_xml_rpc.py
# SPDX-License-Identifier: MIT

from http.server import BaseHTTPRequestHandler, HTTPServer
import bpy
import threading
import json
import urllib.parse as urlparse

HOST = "127.0.0.1"
PORT = 8000

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
            method = urlparse.urlparse(self.path).path.lstrip('/')
            if request:
                params = request.get('params', [])
                id = request.get('id')
            else:
                params = []
                id = None

            if method == 'list_objects':
                result = self.list_objects(*params)
                response = self.success_response(result, id)
            elif method == 'import_obj':
                result = self.import_obj(*params)
                response = self.success_response(result, id)
            elif method == 'delete_obj':
                result = self.delete_obj(*params)
                response = self.success_response(result, id)
            elif method == 'shutdown':
                self.shutdown()
                response = self.success_response("Server is shutting down", id)
            else:
                response = self.error_response(-32601, f"Method not found: {method}", id)

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
        
    def delete_obj(self, obj_name):
        # Check if the object exists in the scene.
        if obj_name in bpy.data.objects:
            # Deselect all objects.
            bpy.ops.object.select_all(action='DESELECT')

            # Get the object.
            obj = bpy.data.objects[obj_name]

            # Set the object as the active object.
            bpy.context.view_layer.objects.active = obj

            # Select the object.
            obj.select_set(True)

            # Create a new context with the object selected and active.
            override = {'selected_objects': [obj], 'active_object': obj, 'object': obj}

            # Delete the object using the new context.
            bpy.ops.object.delete(override)

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

# Keep the main thread alive.
while True:
    pass