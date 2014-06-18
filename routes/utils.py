def get_fullname(obj):
    module = obj.__module__
    name = obj.__name__
    # If it's class
    return "{}.{}".format(module, name)
