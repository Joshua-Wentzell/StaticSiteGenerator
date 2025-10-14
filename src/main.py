import os
import sys
from util import copy_static_to_public, generate_pages_recursive


def main():
    # Get the basepath from CLI argument, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Define paths
    static_dir = os.path.join(project_root, 'static')
    public_dir = os.path.join(project_root, 'public')
    content_dir = os.path.join(project_root, 'content')
    template_path = os.path.join(project_root, 'template.html')
    
    # Delete everything in public directory and copy static files
    copy_static_to_public(static_dir, public_dir)
    
    # Generate all HTML pages from markdown files recursively
    generate_pages_recursive(content_dir, template_path, public_dir, basepath)

main()
