import unittest

from util import *

class TestUtil(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://apple.ca")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIn("href", html_node.props.keys(), "Href not in props")
        self.assertEqual(html_node.props["href"], "https://apple.ca")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.apple.com/v/home/ch/images/heroes/iphone-17/hero_iphone_17__c5vvimu9a20y_large_2x.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIn("src", html_node.props.keys(), "Href not in props")
        self.assertEqual(html_node.props["src"], "https://www.apple.com/v/home/ch/images/heroes/iphone-17/hero_iphone_17__c5vvimu9a20y_large_2x.jpg")
        self.assertIn("alt", html_node.props.keys(), "Alt not in props")
        self.assertEqual(html_node.props["alt"], "This is an image node")


if __name__ == "__main__":
    unittest.main()