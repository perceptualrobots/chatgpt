# ChatCompletionMessage(content='Here is a Python program that reads different system role contents, user role contents, and text blocks from files in the "text" directory, makes a request to the OpenAI ChatGPT API for each combination, and saves the response content to files in the "responses" directory:\n\n```python\nimport openai\nimport os\n\n# Set OpenAI API key\nopenai.api_key = \'YOUR_OPENAI_API_KEY\'\n\n# Directory paths\nsystem_roles_dir = \'system_roles\'\nuser_roles_dir = \'user_roles\'\ntext_dir = \'text\'\nresponses_dir = \'responses\'\n\n# Create responses directory if it does not exist\nif not os.path.exists(responses_dir):\n    os.makedirs(responses_dir)\n\ndef read_file(file_path):\n    with open(file_path, \'r\') as file:\n        return file.read()\n\ndef write_file(file_path, content):\n    with open(file_path, \'w\') as file:\n        file.write(content)\n\ndef make_chatgpt_request(system_content, user_content, text_content):\n    prompt = system_content + user_content + text_content\n    response = openai.Completion.create(\n        engine="davinci",\n        prompt=prompt,\n        max_tokens=150\n    )\n    return response.choices[0].text\n\n# Read system roles content\nsystem_roles = os.listdir(system_roles_dir)\nuser_roles = os.listdir(user_roles_dir)\ntext_files = os.listdir(text_dir)\n\nfor system_role_file in system_roles:\n    system_content = read_file(os.path.join(system_roles_dir, system_role_file))\n    for user_role_file in user_roles:\n        user_content = read_file(os.path.join(user_roles_dir, user_role_file))\n        for text_file in text_files:\n    
#         text_content = read_file(os.path.join(text_dir, text_file))\n            response_content = make_chatgpt_request(system_content, user_content, text_content)\n            response_file_name = os.path.splitext(text_file)[0] + \'_response.txt\'\n            write_file(os.path.join(responses_dir, response_file_name), response_content)\n```\n\nMake sure to replace `\'YOUR_OPENAI_API_KEY\'` with your actual OpenAI API key. This program will iterate through system role contents, user role contents, and text blocks, make a request to the OpenAI ChatGPT API for each combination, and save the response content to files in the "responses" directory.', role='assistant', function_call=None, tool_calls=None)
# CompletionUsage(completion_tokens=484, prompt_tokens=144, total_tokens=628)



import openai 
import os  
# Set OpenAI API key 
# openai.api_key = \'YOUR_OPENAI_API_KEY\'  
# # Directory paths 
# system_roles_dir = \'system_roles\' 
# user_roles_dir = \'user_roles\' 
text_dir = \'text\' 
responses_dir = \'responses\'  
# Create responses directory if it does not exist 
if not os.path.exists(responses_dir):     
    os.makedirs(responses_dir)  
    def read_file(file_path):     
        with open(file_path, \'r\') as file:         
                  return file.read()  
                  
                  def write_file(file_path, content):     
                    with open(file_path, \'w\') as file:         
                              file.write(content)  
                              
                              def make_chatgpt_request(system_content, user_content, text_content):     prompt = system_content + user_content + text_content     response = openai.Completion.create(         engine="davinci",         prompt=prompt,         max_tokens=150     )     return response.choices[0].text  # Read system roles content system_roles = os.listdir(system_roles_dir) user_roles = os.listdir(user_roles_dir) text_files = os.listdir(text_dir)  for system_role_file in system_roles:     system_content = read_file(os.path.join(system_roles_dir, system_role_file))     for user_role_file in user_roles:         user_content = read_file(os.path.join(user_roles_dir, user_role_file))         for text_file in text_files:     
        text_content = read_file(os.path.join(text_dir, text_file))             response_content = make_chatgpt_request(system_content, user_content, text_content)             response_file_name = os.path.splitext(text_file)[0] + \'_response.txt\'             write_file(os.path.join(responses_dir, response_file_name), response_content) ```  Make sure to replace `\'YOUR_OPENAI_API_KEY\'` with your actual OpenAI API key. This program will iterate through system role contents, user role contents, and text blocks, make a request to the OpenAI ChatGPT API for each combination, and save the response content to files in the "responses" directory.', role='assistant', function_call=None, tool_calls=None)


