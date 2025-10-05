import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node: HTMLNode = HTMLNode("<a>", "Hi", [], {
            "href": "https://example.com",
            "target": "_blank",
        })
        expected_result: str = "href=\"https://example.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), expected_result)

    def test_eq2(self):
        node1: HTMLNode = HTMLNode("<a>", "Hi", [], {
            "href": "https://example.com",
            "target": "_blank",
        })
        node2: HTMLNode = HTMLNode("<p>", "Wow this is a nice paragraph", [node1], {
            "href": "https://shawn.com",
        })
        expected_result: str = "href=\"https://shawn.com\""
        self.assertEqual(node2.props_to_html(), expected_result)

    def test_eq3(self):
        node1: HTMLNode = HTMLNode("<a>", "Hi", [], {
            "href": "https://example.com",
            "target": "_blank",
        })
        node2: HTMLNode = HTMLNode("<p>", "Wow this is a nice paragraph", [node1], {
            "href": "https://shawn.com",
            "target": "_blank",
            "ref": "https://example.com",
        })
        expected_result: str = "href=\"https://shawn.com\" target=\"_blank\" ref=\"https://example.com\""
        self.assertEqual(node2.props_to_html(), expected_result)

if __name__ == "__main__":
    unittest.main()