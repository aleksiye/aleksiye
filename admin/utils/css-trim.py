import os
import sys
import re
from bs4 import BeautifulSoup

#function that compares extracted ids and classes from html file(s) with css selectors
def find_missing_selectors(html_selectors, css_selectors):
    missing_selectors = []

    for selector_type in ["ids", "classes"]:
        for selector in css_selectors[selector_type]:
            if selector not in html_selectors[selector_type]:
                missing_selectors.append(selector)

    return missing_selectors


# Function to extract ids and classes from an HTML file
def extract_ids_and_classes(file):
    # Load the HTML file into Beautiful Soup
    with open(file, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Find all HTML tags with an "id" attribute
    ids = [tag["id"] for tag in soup.find_all() if tag.has_attr("id")]

    # Find all HTML tags with a "class" attribute
    classes = [cls for tag in soup.find_all() if tag.has_attr("class")
               for cls in tag["class"]]
    
    return {"ids": ids, "classes": classes}

# Function to process all HTML files in a directory
def process_html_in_directory(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Initialize the result object
    result = {"ids": [], "classes": []}

    # Process each HTML file in the directory
    for file in files:
        if file.endswith(".html"):
            html_path = os.path.join(directory, file)
            extracted = extract_ids_and_classes(html_path)
            result["ids"].extend(extracted["ids"])
            result["classes"].extend(extracted["classes"])

    return result
    

def extract_css_selectors(file):
    with open(file, "r") as f:
        css_text = f.read()

    pattern = r"(?<!\:\s#)(?<=\.|#)[\w-]+"
    selectors = re.findall(pattern, css_text)

    return {"classes": [s for s in selectors if s.startswith("-") or s[0].isalpha()], "ids": [s for s in selectors if s[0] == "#"]}


# Function to process a single HTML file
def process_file(file):

    return extract_ids_and_classes(html_path)


# Console args input
if len(sys.argv) != 3:
    print("Usage: python my_script.py path/to/html/directory path/to/css/file.css")
    sys.exit()
#elif len(sys.argv) == 1:
  #  sys.argv.append('./')
    # sys.argv.append('./assets/css')
html_path = sys.argv[1]
css_path = sys.argv[2]
print(html_path)
print(css_path)

if os.path.isdir(html_path):
    html_selectors = process_html_in_directory(html_path)
    css_selectors = extract_css_selectors(css_path)
elif os.path.isfile(html_path):
    html_selectors = process_file(html_path)
    css_selectors = extract_css_selectors(css_path)
else:
    print("Invalid directory or file.")

print(find_missing_selectors(html_selectors, css_selectors))
