```bash
# Request to list_objects
curl -X PUT http://127.0.0.1:8000/list_objects -H 'Content-Type: application/json' -d '{"id": 1}'

# Request to import_obj
curl -X PUT http://127.0.0.1:8000/import_obj -H 'Content-Type: application/json' -d '{"params": ["/Users/ernest.lee/Downloads/untitled_rem_p0_10_quadrangulation.obj"], "id": 2}'

# Request to delete_obj
curl -X PUT http://127.0.0.1:8000/delete_obj -H 'Content-Type: application/json' -d '{"params": ["untitled_rem_p0_10_quadrangulation"], "id": 3}'

# Another request to list_objects
curl -X PUT http://127.0.0.1:8000/list_objects -H 'Content-Type: application/json' -d '{"id": 4}'

```