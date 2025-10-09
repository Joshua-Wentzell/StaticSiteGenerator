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
