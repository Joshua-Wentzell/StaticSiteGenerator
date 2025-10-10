class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        props_str: str = ""
        if self.props == None:
            return ""
        for key, value in self.props.items():
            props_str += f'{str(key)}="{str(value)}" '
        return str.strip(props_str)

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
