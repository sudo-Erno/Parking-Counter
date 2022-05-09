def get_coordinates():
    with open('utils\slots_coordinates.txt') as file:
        return file.readlines()

# names = []


# if __name__ == '__main__':
#     text = get_coordinates()
#     count = 1
#     letter = "a"
#     old_letter = "2"

#     for line in text:
#         if len(line) == 3: # There is a letter
#             letter = line[:-1]
#             if letter != old_letter:
#                 count = 1
#                 old_letter = letter
#             continue
        
#         x = f"{letter}{count},{line[:-1]}\n"
#         names.append(x)
#         count += 1

#     with open("xddd.txt", "w") as f:
#         for n in names:
#             f.writelines(n)