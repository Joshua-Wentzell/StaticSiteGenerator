from typing import List

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have an 'tag' attribute")
        if self.children is None:
            raise ValueError("ParentNode must have at least one child node")
        html_tag = ""
        if self.props:
            html_tag += f"<{self.tag} {self.props_to_html()}>"
        else :
            html_tag += f"<{self.tag}>"
        for child in self.children:
            html_tag += child.to_html()
        html_tag += f"</{self.tag}>"
        return html_tag