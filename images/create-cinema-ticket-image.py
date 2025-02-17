# Import the OpenAI library
from openai import OpenAI

client = OpenAI()

# Set the prompt
prompt = (
    'Generate an image which is a cinema ticket.'
    'Add the name of the movie as "Gandhi". '
    'Add a banner saying "Perranuthnoe Film Festival". '
    'Add the recipient of the ticket as "Ania Ruszkowski". '
    'Add the date of the ticket as "25 of December 2024". '
    'Add a note saying "VIP Pass".'
)

print(prompt)

# Call the OpenAI image generation API
response = client.images.generate(
    prompt=prompt,
    model="dall-e-3",
    # model="image generator",
    n=1,
    size="1024x1024"
)

# Get the URL of the generated image
for image_data in response.data:
    image_url = image_data.url

    # Print the image URL
    print(image_url)

    # Open the image in the browser
    import webbrowser
    webbrowser.open(image_url)



