
from openai import OpenAI
import os  
import json


def revise_user_content(user_content, word_count, reduction):
	count = word_count
	if reduction > 0:
		count = round( word_count * (100 - reduction) / 100)
		lower_count = round( word_count * (100 - reduction -10) / 100)
		# print(f"Reducing word count by {reduction}% from {word_count} to {count} words.")

		msg = f'Ensure that the generated text is between {lower_count} and {count} words.'
		print (msg)
		user_content = user_content + msg

	return user_content, count


def read_file(file_path):     
  	with open(file_path, 'r') as file:
		  return file.read()  
                  
def write_file(file_path, content):     
	with open(file_path, 'w') as file:         
		file.write(content)  


def is_json(myjson):
  print(myjson)
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

                              
def make_chatgpt_request(system_content, user_content, text_content):     
	# return text_content

	response = client.chat.completions.create(
		 model="gpt-4o",
		 messages=[ 
			 {"role": "system", "content": system_content},
			 {"role": "user", "content": user_content +  text_content}
			 ])     	
	
	# print(response.choices[0].message.content)
	return response.choices[0].message.content  


if __name__ == '__main__':

	client = OpenAI()
	# # Directory paths 
	dir = 'G:\My Drive\PR\Consciousness\chatgpt\paper'
	reduction = 0
	system_roles_dir = dir + os.sep + 'system_roles' 
	user_roles_dir = dir + os.sep + 'user_roles' 
	text_dir = dir + os.sep + 'text' 
	responses_dir = dir + os.sep + 'responses'  
	# Create responses directory if it does not exist 
	if not os.path.exists(responses_dir):     
		os.makedirs(responses_dir)  
	if not os.path.exists(system_roles_dir):     
		os.makedirs(system_roles_dir)  
	if not os.path.exists(user_roles_dir):     
		os.makedirs(user_roles_dir)  
	if not os.path.exists(text_dir):     
		os.makedirs(text_dir)  
	# Read system roles content 

	system_roles = os.listdir(system_roles_dir) 
	user_roles = os.listdir(user_roles_dir) 
	text_files = os.listdir(text_dir)  

	for system_role_file in system_roles:     
		system_prefix = os.path.splitext(system_role_file)[0] 
		system_content = read_file(os.path.join(system_roles_dir, system_role_file))     
		total_word_count = 0
		revised_total_word_count = 0
		response_total_word_count = 0
		for user_role_file in user_roles:         
			user_prefix = os.path.splitext(user_role_file)[0] 
			response_subdir = os.path.join(responses_dir, system_prefix, user_prefix)
			if not os.path.exists(response_subdir):
				os.makedirs(response_subdir)
			user_content = read_file(os.path.join(user_roles_dir, user_role_file))        
			 
			for text_file in text_files:     
				text_content = read_file(os.path.join(text_dir, text_file))         
				word_count = len(text_content.split())
				user_content, revised_count = revise_user_content(user_content, word_count, reduction)
				total_word_count += word_count
				revised_total_word_count += revised_count
				# print(f"Number of words in text_content: {word_count}")
				response_content = make_chatgpt_request(system_content, user_content, text_content)         
				# print(response_content)    
				response_word_count = len(response_content.split())
				print(response_word_count)
				response_total_word_count += response_word_count
				response_file_name = os.path.splitext(text_file)[0] + '_response.txt'             
				write_file(os.path.join(response_subdir, response_file_name), response_content) 
				
		print(f"Total number of words in text_content: original {total_word_count} revised {revised_total_word_count} response {response_total_word_count}")

