import os
from PyPDF2 import PdfReader
import pandas as pd

folder_path = r'G:\My Drive\newideas'  # Your folder path
data = []

for file_name in os.listdir(folder_path):
    if file_name.lower().endswith('.pdf'):
        file_path = os.path.join(folder_path, file_name)
        try:
            # Get file size in kilobytes (KB)
            file_size = os.path.getsize(file_path) / 1024  # Convert bytes to KB

            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                info = reader.metadata
                
                title = info.get('/Title', "N/A") if info else "N/A"
                authors = info.get('/Author', "N/A") if info else "N/A"
                year = info.get('/CreationDate', "N/A")[2:6] if info and '/CreationDate' in info else "N/A"
                data.append([title, authors, year, file_name, f"{file_size:.2f} KB"])
        
        except Exception as e:
            print(f"Error reading {file_name}: {e}")

# Create a DataFrame and save to CSV
df = pd.DataFrame(data, columns=['Title', 'Authors', 'Year', 'File Name', 'File Size'])
df.to_csv('pdf_metadata.csv', index=False)
print("Metadata has been saved to pdf_metadata.csv")
