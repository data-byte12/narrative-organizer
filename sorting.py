import json
import time
import os

# The microservice works inside its own directory
service_dir = "."
request_path = os.path.join(service_dir, "sort-request.json")
response_path = os.path.join(service_dir, "sort-response.json")

print("Sorting microservice running...")

def open_file():
    while True:
        # Read request.json
        try:
            with open(request_path, "r") as f:
                data = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue
    return data

def closing(response_data):
    with open(response_path, "w") as f:
        json.dump(response_data, f, indent=4)
    os.remove(request_path)

def sort_values(sort_list, sort_order):
    if sort_order == "descending":
        sorted_list = sorted(sort_list, reverse=True)
    else:
        sorted_list = sorted(sort_list)
    return {"result": sorted_list}

def sort_by_property(sort_list, sort_property, sort_order):
    if not validate_sort_list(sort_list):
        return {"result": "Error: List format incorrect."}

    if sort_property not in sort_list[0]:
        return {"result": "Error: Property not found in list objects."}

    if sort_order == "descending":
        sorted_list = sorted(sort_list, key=lambda x: x[sort_property], reverse=True)
    else:
        sorted_list = sorted(sort_list, key=lambda x: x[sort_property])
    return {"result": sorted_list}


def validate_sort_list(sort_list):
    for item in sort_list:
        if not isinstance(item, dict):
            return False

    return True


def sort_data():
    data = open_file()
    sort_order = data.get("sort_order")
    sort_property = data.get("sort_property")
    sort_list = data.get("sort_list")

    if sort_order not in ["ascending", "descending"]:
        closing({"result": "Error: Sort order must be 'ascending' or 'descending'."})
        return
    if not sort_list:
        closing({"result": "Error: Sort list is missing."})
        return
    if sort_property:
        response_data = sort_by_property(sort_list, sort_property, sort_order)
    else:
        response_data = sort_values(sort_list, sort_order)

    closing(response_data)
    return

while True:
    sort_data()