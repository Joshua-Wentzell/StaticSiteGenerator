import re
from leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"unknown text node type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        start = 0
        inside_block = False
        block_start = 0
        block_end = 0
        prev_block_start = 0
        while True:
            index = node.text.find(delimiter, start)
            if index == -1:
                if inside_block:
                    raise Exception("Invalid markdown syntax")
                break
            if not inside_block:
                inside_block = True
                block_start = index + len(delimiter)
            else:
                inside_block = False
                block_end = index
                new_node = TextNode(node.text[prev_block_start:block_start - len(delimiter)], TextType.TEXT)
                new_block_node = TextNode(node.text[block_start:block_end], text_type)
                new_nodes.append(new_node)
                new_nodes.append(new_block_node)
                prev_block_start = index + len(delimiter)
            start = index + 1
        last_node = TextNode(node.text[prev_block_start:], TextType.TEXT)
        new_nodes.append(last_node)
    return new_nodes 

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\s\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = list(re.finditer(r"!\[(.*?)\]\((.*?)\)", node.text))
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        last_end = 0
        for match in matches:
            # Add text before the image
            if match.start() > last_end:
                text_before = node.text[last_end:match.start()]
                if text_before and text_before.strip() != "":
                    new_nodes.append(TextNode(text_before, TextType.TEXT))
            
            # Add the image node
            alt_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            last_end = match.end()
        
        # Add remaining text after last image
        if last_end < len(node.text):
            text_after = node.text[last_end:]
            if text_after and text_after.strip() != "":
                new_nodes.append(TextNode(text_after, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = list(re.finditer(r"\s\[(.*?)\]\((.*?)\)", node.text))
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        last_end = 0
        for match in matches:
            # Add text before the image
            if match.start() > last_end:
                text_before = node.text[last_end:match.start() + 1]
                if text_before and text_before.strip() != "":
                    new_nodes.append(TextNode(text_before, TextType.TEXT))
            
            # Add the image node
            alt_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            
            last_end = match.end()
        
        # Add remaining text after last image
        if last_end < len(node.text):
            text_after = node.text[last_end:]
            if text_after and text_after.strip() != "":
                new_nodes.append(TextNode(text_after, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    nodes = [text_node]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for i in range(0, len(blocks)):
        if blocks[i].strip() == "":
            continue
        final_blocks.append(blocks[i].strip())
    return final_blocks