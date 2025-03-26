from openai import OpenAI
import docx
import os
from PyPDF2 import PdfReader


def read_file_content(file_path):
    """
    Reads the content of a file based on its format.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: The content of the file as a string.
    """
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == ".txt":
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_extension.lower() == ".pdf":
        reader = PdfReader(file_path)
        return " ".join(page.extract_text() for page in reader.pages)
    elif file_extension.lower() == ".docx":
        doc = docx.Document(file_path)
        return " ".join(paragraph.text for paragraph in doc.paragraphs)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def summarize_article(file_path):
    """
    Summarizes an academic article and provides its BibTeX citation.

    Args:
        file_path (str): Path to the academic article.

    Returns:
        str: A string containing the summary and BibTeX citation.
    """
    # Read the content of the article
    article_content = read_file_content(file_path)

    # Define the system role and user prompt
    system_role = "You are an expert academic specializing in summarizing research papers."
    user_prompt = (
        f"Summarize this academic article by identifying its main thesis, key arguments, "
        f"and any objections or counterarguments it addresses. Provide a clear and concise "
        f"explanation of the author's reasoning, including any philosophical concepts or theories "
        f"they rely on. If relevant, highlight the implications of the argument and how it contributes "
        f"to the broader discussion. Also get its BibTeX citation:\n\n"
        f"{article_content}"
    )

    # Query the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Extract the summary and BibTeX citation from the response
    result = response.choices[0].message.content
    return result

def save_to_word(results, output_file):
    """
    Saves the summaries and BibTeX citations to a Word document.

    Args:
        results (list): A list of summaries and citations.
        output_file (str): Path to the output Word document.
    """
    doc = docx.Document()

    for idx, result in enumerate(results):
        doc.add_heading(f"Article {idx + 1}", level=1)
        doc.add_paragraph(result)

    doc.save(output_file)

def process_articles(file_paths, output_file):
    """
    Processes a list of academic articles and saves the results to a Word document.

    Args:
        file_paths (list): List of file paths to the academic articles.
        output_file (str): Path to the output Word document.
    """
    results = []
    for file_path in file_paths:
        print(f"Processing: {file_path}")
        try:
            result = summarize_article(file_path)
            results.append(result)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    save_to_word(results, output_file)

if __name__ == "__main__":
    # Example usage
    client = OpenAI()
    article_paths = [
        # "C:/Users/ruper/Dropbox/documents/PR-PCT/papers/consciousness/newideas/1626.full.pdf",
        # "C:/Users/ruper/Dropbox/documents/PR-PCT/papers/consciousness/newideas/Chengzhen Liu 2016.pdf",
        # "C:/Users/ruper/Dropbox/documents/PR-PCT/papers/consciousness/newideas/martin2021.pdf"
        "C:/Users/ruper/Dropbox/documents/PR-PCT/papers/consciousness/newideas/PIIS0896627322006699.pdf"
    ]
    output_doc = "C:/Users/ruper/Dropbox/documents/PR-PCT/papers/consciousness/newideas/summaries.docx"
    process_articles(article_paths, output_doc)
    print(f"Summaries saved to {output_doc}")