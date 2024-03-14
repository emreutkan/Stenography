def green_string(text):

    return f"\033[32m{text}\033[0m"

def write_to_image(file_path):
    input_text = input('Enter your input to be hidden into the image: ')
    selection = input(f"{green_string(input_text)} will be written to the image. Do you want to continue? (y/n): ")
    if selection.lower() != 'y':
        print('Operation cancelled.')
        return
    input_text_as_byte = input_text.encode('utf-8')
    try:
        with open(file_path, 'ab') as f:
            f.write(input_text_as_byte)
    except FileNotFoundError:
        print('Error: The file was not found.')
    except PermissionError:
        print('Error: Permission denied when accessing the file.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        input('Press any key to continue...')


def read_from_image_JPEG(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            jpeg_offset = content.index(bytes.fromhex('FFD9'))
            f.seek(jpeg_offset + 2)
            print(f"{file_path} contains the following hidden message: ")
            print(f.read().decode('utf-8'))
            input('Press any key to continue...')
    except FileNotFoundError:
        print('Error: The file was not found.')
    except ValueError:
        print('Error: Could not find the end of image marker in the JPEG file.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        input('Press any key to continue...')


def delete_from_image_JPEG(file_path):
    try:
        with open(file_path, 'r+b') as f:
            content = f.read()
            jpeg_offset = content.index(bytes.fromhex('FFD9'))
            f.seek(jpeg_offset + 2)
            f.truncate()
    except FileNotFoundError:
        print('Error: The file was not found.')
    except ValueError:
        print('Error: Could not find the end of image marker in the JPEG file.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        input('Press any key to continue...')


def read_from_image_PNG(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            png_offset = content.index(bytes.fromhex('49454E44AE426082'))
            f.seek(png_offset + 8)
            print(f"{file_path} contains the following hidden message: ")
            print(f.read().decode('utf-8'))
            input('Press any key to continue...')
    except FileNotFoundError:
        print('Error: The file was not found.')
    except ValueError:
        print('Error: Could not find the PNG end of file marker.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        input('Press any key to continue...')

def delete_from_image_PNG(file_path):
    try:
        with open(file_path, 'r+b') as f:
            content = f.read()
            png_offset = content.index(bytes.fromhex('49454E44AE426082'))
            f.seek(png_offset + 8)
            f.truncate()
    except FileNotFoundError:
        print('Error: The file was not found.')
    except ValueError:
        print('Error: Could not find the PNG end of file marker.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        input('Press any key to continue...')


def get_file_type_from_extension(file_path):
    if file_path.endswith(('.png', '.PNG')):
        return 'PNG'
    elif file_path.endswith(('.jpeg', '.jpg', '.JPEG', '.JPG')):
        return 'JPEG'
    else:
        return 'Unsupported file type'


def select_file_path():
    file_path = input('Enter the File path (supports drag and drop) : ').strip().replace('"', '').replace("'", "")

    return file_path

if __name__ == "__main__":
    print("\nOptions:")
    print("1. Write to image")
    print("2. Delete from image")
    print("3. Read from image")
    print("4. Change file path")
    print("5. Exit")
    while True:
        print("type 'h' to show options ")
        command = input('Enter a command (1-5): ')

        if command == 'h':
            print("\nOptions:")
            print("1. Write to image")
            print("2. Delete from image")
            print("3. Read from image")
            print("4. Change file path")
            print("5. Exit")
            print("5. Exit")
        elif command == '1':
            write_to_image(file_path)
        elif command == '2':
            extension = get_file_type_from_extension(file_path)
            if extension == 'JPEG':
                delete_from_image_JPEG(file_path)
            elif extension == 'PNG':
                delete_from_image_PNG(file_path)
            else:
                print('Unsupported file type.')
        elif command == '3':
            extension = get_file_type_from_extension(file_path)
            if extension == 'JPEG':
                print('Found JPEG Image')
                print(read_from_image_JPEG(file_path))
            elif extension == 'PNG':
                print('Found PNG Image')
                print(read_from_image_PNG(file_path))
            else:
                print('Unsupported file type.')
        elif command == '4':
            file_path = input('Enter the new file path: ')
        elif command == '5':
            print('Exiting the program.')
            break
        else:
            print('Invalid command. Please enter a number between 1 and 5.')