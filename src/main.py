import os
from textnode import TextType, TextNode
from util import copy_static_to_public


def main():
    # Example usage of the copy_static_to_public function
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    static_dir = os.path.join(project_root, 'static')
    public_dir = os.path.join(project_root, 'public')
    
    print("Starting static file copy...")
    copy_static_to_public(static_dir, public_dir)
    print("Static file copy complete!")
    
    # Previous example code
    text_node = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(text_node)

main()
