from openai import OpenAI  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit images
from IPython.display import display  # used to display images in Jupyter notebooks

client = OpenAI()


# set a directory to save DALL·E images to
image_dir_name = "images/robots"
image_dir = os.path.join(os.curdir, image_dir_name)

# create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# print the directory to save to
print(f"{image_dir=}")


# mode = "robot_hoover"
mode = "robot_arm"

if mode == "robot_hoover":
    # Set the prompt
    prompt = "Generate an image with a blank, transparent background of the elevation view of a robot vacuum cleaner facing from left to right. The robot hoover should be grey and have a circular shape."  

if mode == "robot_four":
    # Set the prompt
    prompt = "Generate an image with a blank, transparent background of the side view of a technical diagram of a simple four-legged robot that looks like the Spot robot facing to the left of the image. The color of the robot should be grey."  

if mode == "robot_arm":
    # Set the prompt
    prompt = "Generate an image with a blank, transparent background of the side view of a technical diagram of an industrial robot arm facing to the left of the image. The color of the robot should be grey."  


# call the OpenAI API
generation_response = client.images.generate(
    model = "dall-e-3",
    prompt=prompt,
    n=1,
    size="1024x1024",
    response_format="url",
)

# print response
print(generation_response)



# save the image
generated_image_name = f'{mode}.png'  # any name you like; the filetype should be .png
generated_image_filepath = os.path.join(image_dir, generated_image_name)
generated_image_url = generation_response.data[0].url  # extract image URL from response
generated_image = requests.get(generated_image_url).content  # download the image

with open(generated_image_filepath, "wb") as image_file:
    image_file.write(generated_image)  # write the image to the file


# print the image
print(generated_image_filepath)
# display(Image.open(generated_image_filepath))


# create variations

# call the OpenAI API, using `create_variation` rather than `create`
variation_response = client.images.create_variation(
    image=generated_image,  # generated_image is the image generated above
    n=2,
    size="1024x1024",
    response_format="url",
)

# print response
print(variation_response)


# save the images
variation_urls = [datum.url for datum in variation_response.data]  # extract URLs
variation_images = [requests.get(url).content for url in variation_urls]  # download images
variation_image_names = [f"{mode}_variation_image_{i}.png" for i in range(len(variation_images))]  # create names
variation_image_filepaths = [os.path.join(image_dir, name) for name in variation_image_names]  # create filepaths
for image, filepath in zip(variation_images, variation_image_filepaths):  # loop through the variations
    with open(filepath, "wb") as image_file:  # open the file
        image_file.write(image)  # write the image to the file



# print the new variations
for variation_image_filepaths in variation_image_filepaths:
    print(variation_image_filepaths)
    display(Image.open(variation_image_filepaths))



