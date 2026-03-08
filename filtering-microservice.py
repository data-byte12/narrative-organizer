import json
import time
import os

# The microservice works inside its own directory
service_dir = os.path.dirname(os.path.abspath(__file__))
request_path = os.path.join(service_dir, "request.json")
response_path = os.path.join(service_dir, "response.json")

print("Filtering microservice running...")

def apply_filter(entry, f):
    field = f.get("field")
    op = f.get("op", "eq")
    value = f.get("value")

    if field not in entry:
        return False

    entry_val = entry[field]

    if op == "eq":
        return entry_val == value
    elif op == "ne":
        return entry_val != value
    elif op == "gt":
        return entry_val > value
    elif op == "lt":
        return entry_val < value
    elif op == "gte":
        return entry_val >= value
    elif op == "lte":
        return entry_val <= value
    elif op == "contains":
        if isinstance(entry_val, str):
            return str(value).lower() in entry_val.lower()
        elif isinstance(entry_val, list):
            return value in entry_val
        return False
    else:
        return False


def write_response(response_data):
    with open(response_path, "w") as f:
        json.dump(response_data, f, indent=4)
    os.remove(request_path)


while True:
    try:
        with open(request_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        time.sleep(0.1)
        continue

    entries = data.get("data")
    filters = data.get("filters")

    # Validate inputs
    if not isinstance(entries, list):
        response_data = {"status": "error", "result": "Error: 'data' must be a list."}
        write_response(response_data)
        continue

    if not isinstance(filters, list):
        response_data = {"status": "error", "result": "Error: 'filters' must be a list of filter objects."}
        write_response(response_data)
        continue

    # Apply all filters (AND logic — entry must match every filter)
    matched = [
        entry for entry in entries
        if isinstance(entry, dict) and all(apply_filter(entry, f) for f in filters)
    ]

    response_data = {"status": "ok", "result": matched}
    write_response(response_data)
