

def write_to_image(file_path):
    input_text = input('Enter your input to be hidden in to image')
    input_text_as_byte = input_text.encode('utf-8')
    with open(file_path, 'ab') as f:
        f.write(input_text_as_byte)

def read_from_image_JPEG(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        jpeg_offset = content.index(bytes.fromhex('FFD9'))
        f.seek(jpeg_offset + 2) 
        return f.read()

def delete_from_image_JPEG(file_path):
    with open(file_path, 'r+b') as f:
        content = f.read()
        jpeg_offset = content.index(bytes.fromhex('FFD9'))
        f.seek(jpeg_offset + 2) 
        f.truncate()
def read_from_image_PNG(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        png_offset = content.index(bytes.fromhex('49454E44AE426082'))
        f.seek(png_offset + 8)
        return f.read()

def delete_from_image_PNG(file_path):
    with open(file_path, 'r+b') as f:
        content = f.read()
        png_offset = content.index(bytes.fromhex('49454E44AE426082'))
        f.seek(png_offset + 8)
        f.truncate()

import os
def get_file_type_from_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()

def main():
    file_path = input('Enter the new file path: ')

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
        elif command == '1':
            write_to_image(file_path)
        elif command == '2':
            extension = get_file_type_from_extension(file_path)
            if 'JPEG' or 'JPG' in extension:
                delete_from_image_JPEG(file_path)
            elif 'PNG' in extension:
                delete_from_image_PNG(file_path)
            else:
                print('Unsupported file type.')
        elif command == '3':
            extension = get_file_type_from_extension(file_path)
            if 'JPEG' or 'JPG' in extension:
                read_from_image_JPEG(file_path)
            elif 'PNG' in extension:
                read_from_image_PNG(file_path)
            else:
                print('Unsupported file type.')
        elif command == '4':
            file_path = input('Enter the new file path: ')
        elif command == '5':
            print('Exiting the program.')
            break
        else:
            print('Invalid command. Please enter a number between 1 and 5.')

if __name__ == "__main__":
    main()