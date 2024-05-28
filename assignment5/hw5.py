import numpy as np
from PIL import Image

def load_color_image(file_path):
    with Image.open(file_path) as img:
        img = img.convert('RGB')
        r, g, b = img.split()
        return np.array(r), np.array(g), np.array(b)

def get_image_size(file_path):
    with Image.open(file_path) as img:
        return img.size  # return (width, height)

def rle_encode(channel):
    pixels = channel.flatten()
    encoded_pixels = []
    prev_pixel = pixels[0]
    count = 1

    for pixel in pixels[1:]:
        if pixel == prev_pixel:
            count += 1
        else:
            encoded_pixels.append((prev_pixel, count))
            prev_pixel = pixel
            count = 1

    # Add the last run
    encoded_pixels.append((prev_pixel, count))
    return encoded_pixels

def save_rle_encoded_file(r_encoded, g_encoded, b_encoded, filename):
    with open(filename, 'w') as file:
        file.write('R\n')
        for value, count in r_encoded:
            file.write(f"{value} {count}\n")
        file.write('G\n')
        for value, count in g_encoded:
            file.write(f"{value} {count}\n")
        file.write('B\n')
        for value, count in b_encoded:
            file.write(f"{value} {count}\n")

def load_rle_encoded_file(filename):
    r_encoded = []
    g_encoded = []
    b_encoded = []
    current_channel = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == 'R':
                current_channel = r_encoded
            elif line == 'G':
                current_channel = g_encoded
            elif line == 'B':
                current_channel = b_encoded
            else:
                value, count = line.split()
                current_channel.append((int(value), int(count)))
    
    return r_encoded, g_encoded, b_encoded

def rle_decode(encoded_pixels, shape):
    decoded_pixels = []
    for value, count in encoded_pixels:
        decoded_pixels.extend([value] * count)
    return np.array(decoded_pixels).reshape(shape)

def show_color_image(r_channel, g_channel, b_channel):
    r_img = Image.fromarray(np.uint8(r_channel), 'L')
    g_img = Image.fromarray(np.uint8(g_channel), 'L')
    b_img = Image.fromarray(np.uint8(b_channel), 'L')
    img = Image.merge('RGB', (r_img, g_img, b_img))
    img.show()

def calculate_size(encoded_pixels):
    return sum(len(f"{value} {count}\n".encode('utf-8')) for value, count in encoded_pixels)

def main():
    compressed_ratios = []
    image_path = 'image/'  # 替換成你的圖片文件路徑
    image_file_name = 'img'+ str(i) +'.bmp'
    file_name = image_path + image_file_name
    output_file_name = 'compressed_' + image_file_name.split('.')[0] + '.bin'

    # get image size
    image_width, image_height = get_image_size(file_name)
    image_shape = (image_height, image_width)

    # load color image and split into R, G, B channels
    r_channel, g_channel, b_channel = load_color_image(file_name)

    # original size
    original_size = r_channel.size + g_channel.size + b_channel.size
    print(file_name + f" >> Original size: {original_size} bytes")

    # compress R, G, B channels
    rle_encoded_r = rle_encode(r_channel)
    rle_encoded_g = rle_encode(g_channel)
    rle_encoded_b = rle_encode(b_channel)

    # save compressed data to file
    save_rle_encoded_file(rle_encoded_r, rle_encoded_g, rle_encoded_b, output_file_name)

    # calculate compressed size
    compressed_size_r = calculate_size(rle_encoded_r)
    compressed_size_g = calculate_size(rle_encoded_g)
    compressed_size_b = calculate_size(rle_encoded_b)
    compressed_size = compressed_size_r + compressed_size_g + compressed_size_b
    print(file_name +f" >> Compressed size: {compressed_size} bytes")

    # check if compression is efficient
    if compressed_size < original_size:
        compressed_ratio = original_size / compressed_size
        print(file_name + f" >> Compression successful, Compression ratio is "+ str(compressed_ratio) +" bytes")
        compressed_ratios.append(compressed_ratio)
    else:
        print("Compression not efficient, compressed size is larger or equal to original size")

    # load compressed data from file
    rle_encoded_r, rle_encoded_g, rle_encoded_b = load_rle_encoded_file(output_file_name)

    decoded_r = rle_decode(rle_encoded_r, image_shape)
    decoded_g = rle_decode(rle_encoded_g, image_shape)
    decoded_b = rle_decode(rle_encoded_b, image_shape)

    # show the color image
    show_color_image(decoded_r, decoded_g, decoded_b)
    return compressed_ratios
    
if __name__ == "__main__":
    compressed_ratios = []
    for i in range(1,4):
        compressed_ratios.extend(main())  # append the compressed ratio to the list

    total_compressed_ratio = sum(compressed_ratios)  # calculate the total compressed ratio
    average = total_compressed_ratio / len(compressed_ratios)  # calculate the average compressed ratio
    print("Average Compression ratio is " + str(average))