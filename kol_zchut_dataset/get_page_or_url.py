import os
import json
import random
import urllib.parse

from kol_zchut_dataset.to_markdown import page_to_markdown

# Load the page_id_to_url mapping
mapping_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "page_id_to_url.jsonl"))
try:
    with open(mapping_file, "r", encoding="utf-8") as f:
        url_to_pagefilename = {json.loads(line)["url"]: json.loads(line)["file_name"] for line in f}
except FileNotFoundError:
    print(f"Mapping file not found at {mapping_file}")

def url_to_page(url):
    # Check if the website URL is in the mapping
    page_id = url_to_pagefilename.get(url)
    if page_id:
        # Load the corresponding page content
        page_file = os.path.abspath(os.path.join(os.path.dirname(__file__), page_id))
        try:
            with open(page_file, "r", encoding="utf-8") as f:
                page_content = f.read()
                return page_content
        except FileNotFoundError:
            print(f"Page file not found for ID {page_id}")
    else:
        print("The entered URL is not in the Kol Zchut dataset.")

if __name__ == "__main__":
    # url = random.choice(list(url_to_pagefilename.keys()))
    # print(url)
    url = "https://www.kolzchut.org.il/he/%D7%94%D7%AA%D7%99%D7%99%D7%A9%D7%A0%D7%95%D7%AA_%D7%97%D7%95%D7%91_%D7%90%D7%A8%D7%A0%D7%95%D7%A0%D7%94_%D7%91%D7%97%D7%9C%D7%95%D7%A3_7_%D7%A9%D7%A0%D7%99%D7%9D"
    print(url)
    url = urllib.parse.unquote(url)
    print(url)
    # url = url.encode('unicode-escape').decode('ascii')
    # print(url)
    pagefilename = url_to_pagefilename.get(url)
    page_content = url_to_page(url)

    import webbrowser

    if page_content:
        # # Write the page content to a temporary file
        # temp_file = os.path.join(os.path.dirname(__file__), "temp_page.html")
        # with open(temp_file, "w", encoding="utf-8") as f:
        #     f.write(page_to_markdown(pagefilename))
        #
        # # Open the temporary file in the browser
        # webbrowser.open(f"file://{temp_file}")
        
        # Open the page content in markdown format
        markdown_temp_file = os.path.join(os.path.dirname(__file__), "temp_page.md")
        with open(markdown_temp_file, "w", encoding="utf-8") as f:
            f.write(page_to_markdown(pagefilename))

        # Open the markdown file in the default system editor
        webbrowser.open(f"file://{markdown_temp_file}")
    else:
        print("Could not fetch the page content.")
    # print(page_content)