import sys


def read_file(file_name='data.txt'):
    """ Example of file name 'data.txt' """
    with open(file_name, "r") as fichier:
        file = fichier.read()
    return file


if __name__ == "__main__":
    # Get file to inspect
    file_name = sys.argv[1]
    print(file_name)

    # Parse it
    file = read_file(file_name)
    nb_lines = len(file.split('\n'))

    # Display results
    print('Number of lines : {}'.format(nb_lines))
