
from openai import OpenAI
import os  
import json


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
	dir = 'C:/files/personal/myfiles/book/latex/book050602'
	system_content = 'You are an expert science fiction writer and literary mimic. \
		You can rewrite text in the distinct voice and stylistic manner of notable science fiction and literary authors \
		such as Isaac Asimov, Ursula K. Le Guin, William Gibson, Octavia Butler, Arthur C. Clarke, and others. \
		You preserve the core narrative and character arcs while adapting prose, tone, pacing, and diction to match the target author.'
	
	# user_content = 'My book is called "Immortal Download" and is a satirical, science-fiction novel set in the year 2044 \
	# 	in the tradition of Blade Runner, The Terminator and The Six Million Dollar Man: a tale of greed, corruption, \
	# 	absolute power, self-exploration, lost humanity, love and, ultimately, redemption. The main character, "Jack Churchill", \
	# 	wakes up to find his mind has been downloaded in to an android replica of himself. Rewrite this chapter in the style of the following authors. \
	# 	For each version, adapt the tone and language to match their literary voice while keeping the plot intact and retaining the storyline and events, and keep a similar word count: \
	# 	Isaac Asimov, Philip K. Dick, Ernest Hemingway and Dan Brown.'

	authors = ['Isaac Asimov', 'Philip K Dick', 'Ernest Hemingway', 'Dan Brown']
	text_file = 'Resurrection.tex'
	text_content = read_file(os.path.join(dir, text_file))         


	for author in authors:
		user_content = f'My book is called "Immortal Download" and is a satirical, science-fiction novel set in the year 2044 \
		in the tradition of Blade Runner, The Terminator and The Six Million Dollar Man: a tale of greed, corruption, \
		absolute power, self-exploration, lost humanity, love and, ultimately, redemption. The main character, "Jack Churchill", \
		wakes up to find his mind has been downloaded in to an android replica of himself. \
		Rewrite this chapter in the style of {author} while retaining the  word count. \
		Preserve the plot, character details, storyline and events, but adapt the tone and language to match their literary voice.'

		response_content = make_chatgpt_request(system_content, user_content, text_content)

		response_dir = os.path.join(dir, 'responses', author.replace(' ', ''))  
		# Create responses directory if it does not exist 
		if not os.path.exists(response_dir):     
			os.makedirs(response_dir)

		write_file(os.path.join(response_dir, text_file), response_content)
        
		print(f"Written response to {response_dir}/{text_file}.")


