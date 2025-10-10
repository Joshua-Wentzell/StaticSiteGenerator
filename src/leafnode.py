from htmlnode import HTMLNode
from typing import Optional

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: Optional[dict[str, str]] = None):
        super().__init__(tag, value, [], props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Value cannot be None")
        if self.tag is None:
            return self.value
        html_tag = ""
        if self.props:
            html_tag += f"<{self.tag} {self.props_to_html()}>"
        else:
            html_tag += f"<{self.tag}>"
        html_tag += self.value
        html_tag += f"</{self.tag}>"
        return html_tag
