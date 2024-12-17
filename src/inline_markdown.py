import re

from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,"**",text_type=TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"*",text_type=TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`",text_type=TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes =[]
    for node in old_nodes:
        
        if node.text_type != TextType.TEXT: # check to make sure it is a text node
            new_nodes.append(node)
            continue # skip rest of this loop cycle
        
        parts = node.text.split(delimiter)  # Split by the bold marker (**)
        if len(parts) == 1: # return a single text node if no bold found
            new_nodes.append(TextNode(parts[0],TextType.TEXT))
            continue
            
        # check to make sure there is an odd number of elements
        if len(parts) % 2 == 0:
            raise ValueError("Missing closing delimiter")
        
        # Loop through parts
        inside_delimiter = False  # Tracks whether the current part is bold or normal
        for part in parts:
            if part:  # Ignore empty parts caused by consecutive markers
                new_nodes.append(TextNode(part, text_type if inside_delimiter else TextType.TEXT))
            inside_delimiter = not inside_delimiter  # Toggle between bold and normal
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes =[]

    # IMAGES
    for node in old_nodes:
        # check to make sure it is a text node
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue
        markdown_images = extract_markdown_images(node.text)
        # if no links return node unchanged
        if not markdown_images: #  and not markdown_links
            new_nodes.append(node)
            continue
        node_remaining = node
        count = len(markdown_images)
        for image in markdown_images:
            sections = node_remaining.text.split(f"![{image[0]}]({image[1]})", 1)
            # text
            if sections[0] != '':
                # add text node to new nodes
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            # image
            new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
            # text
            count = count - 1
            node_remaining = TextNode(sections[1],TextType.TEXT)
            if sections[1] != '' and count < 1:
                # add text node to new nodes
                new_nodes.append(node_remaining)

    return new_nodes

def split_nodes_link(old_nodes):
    
    new_nodes =[]

    # IMAGES
    for node in old_nodes:
        # check to make sure it is a text node
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue
        markdown_links = extract_markdown_links(node.text)
        # if no links return node unchanged
        if not markdown_links: #  and not markdown_links
            new_nodes.append(node)
            continue
        node_remaining = node
        count = len(markdown_links)
        for link in markdown_links:
            sections = node_remaining.text.split(f"[{link[0]}]({link[1]})", 1)
            # text
            if sections[0] != '':
                # add text node to new nodes
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            # link
            new_nodes.append(TextNode(link[0],TextType.LINK,link[1]))
            # text
            count = count - 1
            node_remaining = TextNode(sections[1],TextType.TEXT)
            if sections[1] != '' and count < 1:
                # add text node to new nodes
                new_nodes.append(node_remaining)
            
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)