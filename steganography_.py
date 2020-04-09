from PIL import Image
import time


def readfile(filename):
    file = ''
    x = True
    while x == True:
        try:
            fp = open(filename)
            x = False
        except:
            print('File not found.')
            filename = input("The name of the txt file: ")
    for line in fp:
        line = line.strip()
        if line:
            file += line
    return file


def open_image(image_name):
    x = True
    while x == True:
        try:
            fp = Image.open(image_name)
            x = False
        except:
            print('File not found.')
            image_name = input("The name of the image file: ")
    return fp, image_name

def encode_string(string):
    bi_string = ''
    for ch in string:
        num = to_binary(ord(ch))
        bi_string += str(num).zfill(8)
    bi_string += '010000110111010001110010011011000010110101000100'

    return bi_string

def encode_image(image, bi_string):
    im, image = open_image(image)
    w, h = im.size
    pix = im.load()
    count = 0
    start = time.time()
    for i in range(w):
        if count >= len(bi_string):
                break
        for j in range(h):
            rgb = pix[i,j]
            r = to_binary(rgb[0])
            g = to_binary(rgb[1])
            b = to_binary(rgb[2])

            if count < len(bi_string):
                if bi_string[count] == '1':
                    r = r[:-1] + '1'
                else:
                    r = r[:-1] + '0'

            count += 1

            if count < len(bi_string):
                if bi_string[count] == '1':
                    g = g[:-1] + '1'
                else:
                    g = g[:-1] + '0'

            count += 1

            if count < len(bi_string):
                if bi_string[count] == '1':
                    b = b[:-1] + '1'
                else:
                    b = b[:-1] + '0'
            count += 1

            pix[i,j] = (int(to_decimal(r)), int(to_decimal(g)), int(to_decimal(b)))

            if count >= len(bi_string):
                break
    end = time.time()
    print('Time for PIL:', end - start)
    new_image = str(image[:-4] + "encoded.png")
    im.save(image[:-4]+"encoded.png")
    return new_image

def decode_string(bi_string):
    string = ''
    count = 0
    while count <= (len(bi_string)):
        string += chr(to_decimal(bi_string[count:count+8]))
        count += 8

    string = string[:-7]
    return string

def decode_image(image):
    im, image = open_image(image)
    w, h = im.size
    pix = im.load()
    bi_string = ''
    for i in range(w):
        for j in range(h):
            rgb = pix[i, j]

            r = to_binary(rgb[0])
            g = to_binary(rgb[1])
            b = to_binary(rgb[2])

            bi_string += r[-1:]
            bi_string += g[-1:]
            bi_string += b[-1:]

            if '010000110111010001110010011011000010110101000100' in bi_string:
                return bi_string

    return bi_string


def to_decimal(num):
    num = list(str(num))

    num.reverse()
    lst = []

    for i in range(len(num)):
        part = int(num[i]) * (2 ** i)
        lst.append(part)

    dec = sum(lst)
    return dec

def to_binary(dec):
    lst = []
    dec = int(dec)
    while dec >= 1:
        rmdr = dec % 2
        dec = int(dec / 2)
        lst.append(str(rmdr))

    lst.reverse()
    binary = ''.join(lst)
    return binary.zfill(8)

def main():
    print('**Decoding only works on previously encoded messages**', '\n')
    
    user_input = input('Encode a message into a picture (e) or decode a message from a picture (d) or quit (q): ').lower()
    print()

    while user_input != 'q':
        if user_input == 'e':
            message = input("Message you would like encoded in the image: ").lower()
            
            if message == 'txt file':
                message = input("The name of the txt file: ")
                message = readfile(message)
            elif message == 'q':
                break
            
            print()
            print('Make sure the image is in the same folder as this program!')
            image_file = input("The name of the image file (Don't forget .jpg or .png): ").lower()
            if image_file == 'q':
                break
            print()
            binary_string = encode_string(message)
            encoded_image = encode_image(image_file, binary_string)
            print("Image encoded. Filename:", encoded_image)
            print()

        if user_input == 'd':
            image_name = input('The name of the encoded image file: ').lower()
            if image_name == 'q':
                break
            decoded_string = decode_image(image_name)
            string = decode_string(decoded_string)
            print()
            print('*'*20, end='')
            print(' ENCODED MESSAGE ', end='')
            print('*'*20)
            print(string)
            print('*'*(40 + len(' ENCODED MESSAGE ')))
            print()
        
        user_input = input('Would you like to encode or decode another image? Yes(y) or No(n) ? ').lower()
        print()
        if user_input == 'n':
            user_input = 'q'

        if user_input == 'y':
            print('**Decoding only works on previously encoded messages**')
            print()
            user_input = input('Encode a message into a picture (e) or decode a message from a picture (d) or quit (q): ').lower()
            
 
    input()  


main()