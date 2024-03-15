import os.path
import subprocess
import sys
from datetime import datetime

file = ''
file_path = ''
file_size = ''
file_extension = ''


def green(text):
    return f"\033[32m{text}\033[0m"


def red(text):
    return f"\033[31m{text}\033[0m"


def yellow(text):
    return f"\033[33m{text}\033[0m"


def blue(text):
    return f"\033[34m{text}\033[0m"


def clear():
    subprocess.run('clear', shell=True)


def get_file_type_from_extension():
    global file_extension
    if file_path.lower().endswith('.png'):
        file_extension = 'PNG'
    elif file_path.lower().endswith(('.jpeg', '.jpg')):
        file_extension = 'JPEG'
    else:
        file_extension = ''


def update_file_size():
    global file_size
    file_size = os.path.getsize(file_path)


def get_file_path():
    clear()
    global file_path, file, file_size
    file_path = input('Enter the File path (supports drag and drop) : ').strip().replace('"', '').replace("'", "")
    try:
        file = file_path.split('/')[-1]
        get_file_type_from_extension()
        if file_extension is '':
            file = ''
            file_path = ''
            print(f'Unsupported file type: {red(file_extension)}')
            print(f'Supported file types: {green(".png, .jpeg, .jpg")}')
            input('Press any key to continue...')
            return False
        else:
            file_size = os.path.getsize(file_path)
    except FileNotFoundError:
        print(red('Error: The file was not found.'))
        input('Press any key to continue...')
        return False


def read_from_image():
    clear()
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            clear()

            if file_extension == 'JPEG':
                jpeg_offset = content.index(bytes.fromhex('FFD9')) + 2
                f.seek(jpeg_offset)
                message = f.read().decode('utf-8')
                if not message:
                    print(f"{blue(file)} does not contain any hidden message.")
                else:
                    print(f"{blue(file)} contains the following hidden message: ")
                    print(green(message))

            elif file_extension == 'PNG':
                png_offset = content.index(bytes.fromhex('49454E44AE426082')) + 8
                f.seek(png_offset)
                message = f.read().decode('utf-8')
                if not message:
                    print(f"{blue(file)} does not contain any hidden message.")
                else:
                    print(f"{blue(file)} contains the following hidden message: ")
                    print(green(message))

    except FileNotFoundError:
        print('Error: The file was not found.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        input('Press any key to continue...')


def delete_from_image():
    clear()
    try:
        with open(file_path, 'r+b') as f:
            content = f.read()
            clear()
            if file_extension == 'JPEG':
                jpeg_offset = content.index(bytes.fromhex('FFD9')) + 2
                f.seek(jpeg_offset)
                message = f.read().decode('utf-8')
                if not message:
                    print(f"{blue(file)} does not contain any hidden message.")
                else:
                    print(f"{green(message)} \nDeleted from {blue(file)}: ")
                    jpeg_offset = content.index(bytes.fromhex('FFD9'))
                    f.seek(jpeg_offset + 2)
                    f.truncate()
                    input('Press any key to continue...')
            elif file_extension == 'PNG':
                png_offset = content.index(bytes.fromhex('49454E44AE426082')) + 8
                f.seek(png_offset)
                message = f.read().decode('utf-8')
                if not message:
                    print(f"{blue(file)} does not contain any hidden message.")
                else:
                    print(f"{green(message)} \nDeleted from {blue(file)}: ")
                    png_offset = content.index(bytes.fromhex('49454E44AE426082'))
                    f.seek(png_offset + 8)
                    f.truncate()
                    input('Press any key to continue...')
    except FileNotFoundError:
        print('Error: The file was not found.')
        input('Press any key to continue...')
        return


def write_to_image():
    clear()
    input_text = input(f'Enter your input to be hidden into the {blue(file)} : ')
    selection = input(f"{green(input_text)} will be written to the {blue(file)}. Do you want to continue? (y/n): ")
    if selection.lower() != 'y':
        print('Operation cancelled.')
        return
    input_text_as_byte = ('| (UTC) ' + str(datetime.utcnow()) + ' : ' + input_text + '\x0A' ).encode()
    try:
        with open(file_path, 'ab') as f:
            f.write(input_text_as_byte)
            clear()
    except FileNotFoundError:
        print('Error: The file was not found.')
    except PermissionError:
        print('Error: Permission denied when accessing the file.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        print(f"{yellow(sys.getsizeof(input_text_as_byte))} bytes of data written to {blue(file)}.")
        input('Press any key to continue...')


if __name__ == "__main__":
    while True:
        clear()
        if not file_path:
            get_file_path()
        else:
            update_file_size()
            print(f'----{yellow("File Information")}----------------')
            print(f"File: {blue(file)}")
            print(f"File path: {blue(file_path)}")
            print(f"File size: {blue(file_size)} bytes")
            print(f"File type: {blue(file_extension)}")
            print(f"UTC Time: {blue(datetime.utcnow())}")
            print(f'----{green("Options")}-------------------------')
            print(f"{green('1)')} Write to image")
            print(f"{green('2)')} Delete from image")
            print(f"{green('3)')} Read from image")
            print(f"{green('4)')} Change file path")
            print(f"{green('5)')} Exit")
            command = input('Enter a command (1-5): ')
            if command == '1':
                write_to_image()
            elif command == '2':
                delete_from_image()
            elif command == '3':
                read_from_image()
            elif command == '4':
                get_file_path()
            elif command == '5':
                print(blue('Exiting.'))
                break
            else:
                print('Invalid command. Please enter a number between 1 and 5.')
