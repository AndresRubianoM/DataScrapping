import yaml


__config = None

def config():
    global __config

    if not __config:
        with open('D:\Andrés\IngenieriaDatos\config.yaml', 'r') as f:
            __config = yaml.load(f, Loader = yaml.BaseLoader)
        
    return __config 