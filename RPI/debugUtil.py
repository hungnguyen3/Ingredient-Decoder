import sys


def PrintToFile(text):
    with open('filename.txt', 'w') as f:
        sys.stdout = f  # Change the standard output to the file we created.
        print(text)
