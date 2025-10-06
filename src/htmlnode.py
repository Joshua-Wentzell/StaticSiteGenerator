from typing import List


class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: List["HTMLNode"] = None, props: dict[str, str] = None):
        self.tag: str = tag
        self.value: str = value
        self.children: List["HTMLNode"] = children
        self.props: dict[str, str] = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        props_str: str = ""
        for key, value in self.props.items():
            props_str += f'{str(key)}="{str(value)}" '
        return str.strip(props_str)

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'