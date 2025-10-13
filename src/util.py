import re
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(markdown_text):
    lines = markdown_text.split('\n')
    
    # Check for heading (starts with 1-6 # followed by space)
    if re.match(r'^#{1,6}\s', markdown_text):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with ```)
    if markdown_text.startswith('```') and markdown_text.endswith('```'):
        return BlockType.CODE
    
    # Check for quote (all lines start with >)
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (all lines start with * or -)
    if all(line.startswith('* ') or line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (all lines start with number. )
    if all(re.match(r'^\d+\.\s', line) for line in lines):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

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
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
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
                # Only add if not just whitespace
                if text_before.strip():
                    new_nodes.append(TextNode(text_before, TextType.TEXT))
            
            # Add the image node
            alt_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            last_end = match.end()
        
        # Add remaining text after last image
        if last_end < len(node.text):
            text_after = node.text[last_end:]
            # Only add if not just whitespace
            if text_after.strip():
                new_nodes.append(TextNode(text_after, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = list(re.finditer(r"(?<!\!)\[(.*?)\]\((.*?)\)", node.text))
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        last_end = 0
        for match in matches:
            # Add text before the link
            if match.start() > last_end:
                text_before = node.text[last_end:match.start()]
                if text_before:
                    new_nodes.append(TextNode(text_before, TextType.TEXT))
            
            # Add the link node
            alt_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            
            last_end = match.end()
        
        # Add remaining text after last link
        if last_end < len(node.text):
            text_after = node.text[last_end:]
            if text_after:
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
    for block in blocks:
        stripped = block.strip()
        if stripped:
            final_blocks.append(stripped)
    return final_blocks

def text_to_children(text):
    # Replace newlines with spaces for inline rendering
    text = text.replace('\n', ' ')
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def heading_to_html_node(block):
    # Count the number of # at the start
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    
    if level < 1 or level > 6:
        raise Exception(f"Invalid heading level: {level}")
    
    # Extract text after the hashes and space
    text = block[level:].strip()
    children = text_to_children(text)
    
    return HTMLNode(f"h{level}", None, children)

def quote_to_html_node(block):
    lines = block.split('\n')
    # Remove > from each line
    cleaned_lines = []
    for line in lines:
        if line.startswith('>'):
            cleaned_lines.append(line[1:].strip())
        else:
            cleaned_lines.append(line)
    
    # Join lines back together
    content = '\n'.join(cleaned_lines)
    children = text_to_children(content)
    
    return HTMLNode("blockquote", None, children)

def unordered_list_to_html_node(block):
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Remove the list marker (- or *)
        if line.startswith('- '):
            text = line[2:]
        elif line.startswith('* '):
            text = line[2:]
        else:
            text = line
        
        # Create list item with inline children
        children = text_to_children(text)
        list_items.append(HTMLNode("li", None, children))
    
    return HTMLNode("ul", None, list_items)

def ordered_list_to_html_node(block):
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Remove the number and period (e.g., "1. ")
        match = re.match(r'^\d+\.\s', line)
        if match:
            text = line[match.end():]
        else:
            text = line
        
        # Create list item with inline children
        children = text_to_children(text)
        list_items.append(HTMLNode("li", None, children))
    
    return HTMLNode("ol", None, list_items)

def code_to_html_node(block):
    # Remove ``` from start and end
    if not (block.startswith('```') and block.endswith('```')):
        code_content = block
    else:
        # Remove the backticks
        code_content = block[3:-3]
        
        # If content starts with newline, it might have a language identifier
        # Check if the first line (before first \n) is just a word (language name)
        if code_content.startswith('\n'):
            # No language identifier, just remove leading newline
            code_content = code_content[1:]
        else:
            # Check if first line is a language identifier
            first_newline = code_content.find('\n')
            if first_newline != -1:
                first_line = code_content[:first_newline]
                # If first line has no spaces and is alphanumeric, it's likely a language
                if first_line.strip() and ' ' not in first_line.strip() and first_line.strip().isalnum():
                    # Skip the language identifier line
                    code_content = code_content[first_newline + 1:]
    
    # Create code node as a leaf node (preserve exact formatting)
    code_node = LeafNode("code", code_content)
    # Wrap in pre tag
    return HTMLNode("pre", None, [code_node])

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.PARAGRAPH:
                child_nodes = text_to_children(block)
                children.append(HTMLNode("p", None, child_nodes))
                
            case BlockType.HEADING:
                heading_node = heading_to_html_node(block)
                children.append(heading_node)
                
            case BlockType.CODE:
                code_node = code_to_html_node(block)
                children.append(code_node)
                
            case BlockType.QUOTE:
                quote_node = quote_to_html_node(block)
                children.append(quote_node)
                
            case BlockType.UNORDERED_LIST:
                list_node = unordered_list_to_html_node(block)
                children.append(list_node)
                
            case BlockType.ORDERED_LIST:
                list_node = ordered_list_to_html_node(block)
                children.append(list_node)
    
    return HTMLNode("div", None, children)