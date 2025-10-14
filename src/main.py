import os
from util import copy_static_to_public, generate_page


def main():
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Define paths
    static_dir = os.path.join(project_root, 'static')
    public_dir = os.path.join(project_root, 'public')
    content_path = os.path.join(project_root, 'content', 'index.md')
    template_path = os.path.join(project_root, 'template.html')
    dest_path = os.path.join(public_dir, 'index.html')
    
    # Delete everything in public directory and copy static files
    copy_static_to_public(static_dir, public_dir)
    
    # Generate index.html from markdown
    generate_page(content_path, template_path, dest_path)

main()
