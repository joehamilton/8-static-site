import os, shutil
import re
from textnode import TextNode,TextType

def main():
    # new_text_node = TextNode("normal",TextType.NORMAL,"https://www.google.com")

    # create public if doesn't exist
    origin_path = os.path.expanduser("~/dev/boot-dev/8-boot-static-site/static")
    destination_path = os.path.expanduser("~/dev/boot-dev/8-boot-static-site/public")
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path) 
    os.mkdir(destination_path) 
    copy_files(origin_path, destination_path)


def copy_files(origin_path, destination_path):
    folder_contents = os.listdir(origin_path)
    for item in folder_contents:
        item_path = os.path.join(origin_path, item)
        # if file
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination_path)
            continue
        # if folder
        new_origin_path = os.path.join(origin_path, item)
        new_destination_path = os.path.join(destination_path, item)
        os.mkdir(new_destination_path)
        # if folder has files
        deeper_folder_files = os.listdir(item_path)
        if deeper_folder_files:
            copy_files(new_origin_path, new_destination_path)

def extract_title(markdown):
    # Use regex to match the first line starting with '# ' (Markdown H1)
    match = re.search(r'^# (.+)', markdown, re.MULTILINE)
    if match:
        return match.group(1).strip() 
    raise ValueError("No H1")

def generate_page(from_path, template_path, dest_path):
    print("Generating page from from_path to dest_path using template_path")
    md_file = open(from_path, 'r')
    md = md_file.read()
    md_file.close()
    template_file = open(template_path, 'r')
    template = template_file.read()
    template_file.close()
    # UP TO HERE


main()
