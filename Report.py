import requests

base_url = "http://127.0.0.1:5000"

print("--- Testing Partner API: Jeepney Route Finder ---")

res_all = requests.get(base_url + "/api/v1/routes")
print("GET all routes:", res_all.status_code)

res_one = requests.get(base_url + "/api/v1/routes/1")
print("GET route 1:", res_one.status_code, res_one.json())

new_route = {
    "route_number": "16",
    "origin": "Mabalacat Terminal",
    "destination": "SM Clark",
    "fare": 15
}
res_post = requests.post(base_url + "/api/v1/routes/create/", json=new_route)
print("POST create route:", res_post.status_code, res_post.json())

updated_route = {
    "origin": "Dau Terminal",
    "destination": "SM Clark",
    "fare": 18
}
res_put = requests.put(base_url + "/routes/update/16", json=updated_route)
print("PUT update route:", res_put.status_code, res_put.json())

res_error = requests.get(base_url + "/api/v1/routes/999")
if res_error.status_code == 404:
    print("Error handled! Route 999 not found (Status 404):", res_error.json())
else:
    print("Unexpected response:", res_error.status_code)

res_delete = requests.delete(base_url + "/api/v1/routes/16")
print("DELETE route 16:", res_delete.status_code)

print("\n--- Summary Report ---")
print("GET /api/v1/routes ->", res_all.status_code)
print("GET /api/v1/routes/1 ->", res_one.status_code)
print("POST /api/v1/routes/create/ ->", res_post.status_code)
print("PUT /routes/update/16 ->", res_put.status_code)
print("GET /api/v1/routes/999 (Error Test) ->", res_error.status_code)
print("DELETE /api/v1/routes/16 ->", res_delete.status_code)