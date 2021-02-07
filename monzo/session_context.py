import json

class MonzoContext:
    access_token = None
    refresh_token = None
    client_id = None
    client_secret = None
    redirect_uri = None
    client_code = None

def load_context(path: str):
    with open(path) as file:
        context = MonzoContext()
        config = json.load(file)
        items = [i for i in dir(context) if not i.startswith("__")]
        for item in items:
            context.__setattr__(item, config[item])
    return context

def to_json(context: MonzoContext):
    items = {i : context.__getattribute__(i) for i in dir(context) if not i.startswith("__")}
    return json.dumps(items, indent=4)

