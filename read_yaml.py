import yaml

path = 'constants.yaml'
def read_yaml():
    with open(path, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)