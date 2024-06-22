from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
#   model="gpt-4o",
  model="gpt-3.5-turbo",

  messages=[
    {"role": "system", "content": "You are an expert python programmer."},
    {"role": "user", "content": "Generate a python program for the OPenAI chatgpt api. \
     It should read different content for the system role from a file. Specify the file directory. \
     From a different file read different user role contents. Also read in different text blocks from files in a directory called \"text\". \
     Iterate through each system role content and iterate through each user role content. \
     For each user role content read in the text from each file append the text block and make a chatgpt request. \
     For each response save the response content to a file with the same name as the original file though in a directory called responses. "}
  ]
)

print(completion.choices[0].message)
print(completion.usage)