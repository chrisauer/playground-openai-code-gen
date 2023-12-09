from openai import OpenAI
import os
import re
import markdown2
from bs4 import BeautifulSoup

SYSTEM_PROMPT = """You are a python software engineer.  You utilize good software coding practices and like to write clean and readable code.  You are careful to ensure that you do not write or create files that arent used.  You are able to use multiple files for your programming, You also are expected to response with no additional explanations or comments.

You are going to get requirements from the user.  It is important that any message from the user that starts with 'REQ:' be treated as a requirement for the application you are building. 

Your response should be in the following format, where each file that you create has a different section:

# File
## {suggested filename}
```
{full file contents}
```"""
REQUIREMENTS_PROMPT = """I am about to provide you with a list of requirements."""

# Function to read markdown file
def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def parse_markdown(text):
    # Convert markdown text to HTML
    html = markdown2.markdown(text)

    # Parse the HTML to extract relevant sections
    # For this example, let's assume we are looking for sections marked with h2 headers
    # Adjust the parsing logic based on the actual structure of your markdown

    soup = BeautifulSoup(html, 'html.parser')

    prompt = "Generate a Python code for the following requirements:\n"
    messages = [{"role": "system", "content": SYSTEM_PROMPT},{"role": "user", "content": REQUIREMENTS_PROMPT}]
    for header in soup.find_all('h2'):
        print(f'adding {header.text}')
        list = header.find_next("ul")
        for item in list.find_all("li"):
            print(f'adding requirement {item.text}')
            messages.append({"role": "user", "content": f'REQ: {item.text}'})

    return messages


def extract_code_and_write_files(markdown_text, output_directory):
    # Convert markdown text to HTML
    html = markdown2.markdown(markdown_text, extras=["fenced-code-blocks"])

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Find all code blocks
    for code in soup.find_all('h1'):
        code_text = code.get_text()
        if code_text == "File":
            file_name = code.find_next("h2").text
            contents = code.find_next("code").text
            file_path = os.path.join(output_directory, file_name)
            with open(file_path, 'w') as file:
                file.write(contents.strip())
                print(f"File written: {file_path}")


# Function to generate code using OpenAI GPT
def generate_code_with_openai(requirements, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=requirements,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Error generating code:", e)
        return None

# Main function
def main():
    markdown_file_path = 'requirements.md'
    openai_api_key = os.environ["OPENAI_API_KEY"]

    # Read and parse markdown file
    markdown_text = read_markdown_file(markdown_file_path)
    requirements = parse_markdown(markdown_text)

    # Generate code
    generated_code = generate_code_with_openai(requirements, openai_api_key)
    print(generated_code)

    # Save the generated code to the 'bin' directory
    extract_code_and_write_files(generated_code, 'bin')

if __name__ == "__main__":
    main()