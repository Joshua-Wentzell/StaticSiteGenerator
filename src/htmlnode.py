class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("HTMLNode requires a tag")
        
        # Build opening tag
        opening = f"<{self.tag}{self.props_to_html()}>"
        
        # Build content
        if self.value is not None:
            content = self.value
        elif self.children:
            content = "".join(child.to_html() for child in self.children)
        else:
            content = ""
        
        # Build closing tag
        closing = f"</{self.tag}>"
        
        return opening + content + closing

    def props_to_html(self) -> str:
        props_str: str = ""
        if self.props == None:
            return ""
        for key, value in self.props.items():
            props_str += f'{str(key)}="{str(value)}" '
        return str.strip(props_str)

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
