def generate_kwargs_for_get_users(**kwargs) -> dict:
    kw = dict()
    for key, value in kwargs.items():
        if value is not None:
            if key == "handles":
                value = value.split(";")
            kw[key] = value
    return kw
