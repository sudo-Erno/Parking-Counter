def get_coordinates():
    with open('utils\parking_coordinates.txt') as file:
        return file.readlines()[1:]

if __name__ == '__main__':
    x = get_coordinates()
    print(x)