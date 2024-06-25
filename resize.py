from PIL import Image

# Load the original JPG image
input_file = 'elephant.jpg'
original_image = Image.open(input_file)

# Define the desired size (e.g., 512x512 pixels)
desired_size = (170, 170)

# Resize the original image to the desired size
resized_image = original_image.resize(desired_size)

# Define the output PPM file name for the resized image
output_file = 'cover.png'

# Save the resized image as a PPM file
resized_image.save(output_file)

print(f'Resize and conversion complete. Saved as {output_file}')
