import numpy


def main():
    inputs = ['a_example.txt', 'b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt', 'e_so_many_books.txt',
              'f_libraries_of_the_world.txt']
    for file in inputs:
        out_file = 'outputs/' + file[0] + '_output.txt'
        in_file = 'inputs/' + file
        print("Running ", file)
        run(in_file, out_file)


def build_libraries(data_arr):
    libs = []
    lib_id = 0
    for lid in range(0, len(data_arr), 2):
        l1 = data_arr[lid].split(' ')
        if len(l1) == 3:
            l2 = data_arr[lid+1].split(' ')

            libs.append({'num_books': int(l1[0]),
                         'signup_len': int(l1[1]),
                         'ship_books': int(l1[2]),
                         'books': l2})
            lib_id += 1
    return libs


def build_efficiancies(libs):
    effs = []
    for lib in libs:
        effs.append(lib['signup_len']/lib['ship_books'])
    return effs


def run(file_in, file_out):
    libraries_signed_up = 0
    lib_position = 0
    # Read input
    data = []
    with open(file_in, "r") as f:
        for line in f:
            data.append(line.rstrip('\n'))

    # create data arrays
    important_info = data.pop(0).split(" ")
    book_scores = data.pop(0).split(" ")

    book_scores = list(map(int, book_scores))

    libraries = build_libraries(data)

    num_books = int(important_info[0])
    num_libraries = int(important_info[1])
    days_left = int(important_info[2])

    # calculate efficiency weighting
    library_efficiencies = build_efficiancies(libraries)

    # create indices list
    lib_indices = list(numpy.argsort(library_efficiencies))

    to_write = ['']

    books_scanned = set()
    score = 0

    while days_left > 0 and int(libraries_signed_up) != len(library_efficiencies):
        pointer = lib_indices[libraries_signed_up].item()
        library_info = libraries[pointer]
        book_info = library_info['books']
        days_left -= library_info['signup_len']

        if days_left > 0:
            book_info_scores = book_info[:]
            for x in range(len(book_info_scores)):
                book_info_scores[x] = book_scores[x]

            sortedlist = list(numpy.argsort(book_info_scores)[::-1])

            booksthatcanbescanned = days_left * library_info['ship_books']

            bookstoscan = ""
            booksent = 0
            if len(sortedlist) < booksthatcanbescanned:
                for book in sortedlist:
                    bookstoscan = bookstoscan + book_info[book] + " "
                    booksent += 1
                    if book_info[book] not in books_scanned:
                        books_scanned.add(book_info[book])
                        score += book_info_scores[book]
            else:
                for x in range(days_left):
                    bookstoscan = bookstoscan + book_info[sortedlist[x]] + " "
                    booksent += 1
                    if book_info[sortedlist[x]] not in books_scanned:
                        books_scanned.add(book_info[sortedlist[x]])
                        score += book_info_scores[sortedlist[x]]

            to_write.append(str(pointer) + " " + str(booksent) + "\n")
            to_write.append(str(bookstoscan) + "\n")

            libraries_signed_up += 1

    to_write[0] = str(libraries_signed_up) + "\n"
    with open(file_out, "w+") as w:
        w.writelines(to_write)

    print("Score: ", score)


if __name__ == '__main__':
    main()
