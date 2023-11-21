def generate_kwargs(**kwargs):
    kw = dict()

    for key, value in kwargs.items():
        if value is not None:
            if key == "_id":
                key = "id"
            if key == "handles":
                value = value.split(";")
            kw[key] = value

    return kw
