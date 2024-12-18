# Import the OpenAI library
from openai import OpenAI

client = OpenAI()

# Set the prompt
prompt = "Generate an image that looks like a cinema ticket for the movie Gandhi. The movie is showing as part of the Perranuthnoe Film Festival. The recipient of the ticket is Ania Ruszkowski. The date of the ticket should be 25 of December 2024."

# Call the OpenAI image generation API
response = client.images.create_variation(
    prompt=prompt,
    n=1,
    size="1024x1024"
)

# Get the URL of the generated image
image_url = response['data'][0]['url']

# Print the image URL
print(image_url)

# Save the image URL to a file
with open("cinema_ticket_image.txt", "w") as file:
    file.write(image_url)



