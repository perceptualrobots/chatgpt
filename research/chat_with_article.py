import argparse
from research.article import ArticleQuery

"""
python -m research.chat_with_article -f "G:/My Drive/newideas/PIIS0960982213001401.pdf" -u "What is the main thesis of this article?" -s "You are an expert academic specializing in summarizing research papers."

python -m research.chat_with_article -f "G:/My Drive/newideas/1626.full.pdf" -u "Here is a document for review." -s "Do not respond with an analysis until specifically questioned to do so."

python -m research.chat_with_article -f "G:/My Drive/newideas/1626.full.pdf" -u "How does the author define perception?." -s "You are an expert in analyzing, reviewing, and summarizing academic documents, specializing in philosophy and psychology with a focus on human behavior and the nature of consciousness. Your goal is to provide clear, insightful, and concise summaries that capture the main thesis, key arguments, counterarguments, and philosophical concepts presented in the text. You should identify the author’s reasoning, theoretical frameworks, and the implications of the arguments within the broader academic discourse. Use precise language and maintain a formal, academic tone while delivering comprehensive and nuanced interpretations of complex ideas."
python -m research.chat_with_article -f "G:/My Drive/newideas/1626.full.pdf" -u "In which sections does the author discuss the defininitions of perception?" 


"""
if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Chat with GPT using an article.")
    parser.add_argument("-f", "--file", required=True, help="Path to the file to process.")
    parser.add_argument("-u", "--user_input", required=True, help="User input for the GPT interaction.")
    parser.add_argument("-s", "--system_message", required=False, help="System message for the GPT interaction.")

    # Parse the arguments
    args = parser.parse_args()

    # Create an instance of ArticleQuery
    article = ArticleQuery()

    # Call the chat_with_gpt method from ArticleQuery
    article.chat_with_gpt(file_path=args.file, user_input=args.user_input, system_message=args.system_message)



