def get_coordinates():
    with open('utils\slots_coordinates.txt') as file:
        return file.readlines()