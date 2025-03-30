import argparse
from research.article import ArticleQuery

"""
python -m research.chat_with_article -f "G:/My Drive/newideas/PIIS0960982213001401.pdf" -u "What is the main thesis of this article?" -s "You are an expert academic specializing in summarizing research papers."
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



