import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    def test_text_diff(self):
        node = TextNode("This is a text node", TextType.BOLD, "test")
        node2 = TextNode("This is a different text node", TextType.BOLD, "test")
        self.assertNotEqual(node, node2)
    def test_same(self):
        node = TextNode("This is a text node", TextType.LINK, "test")
        node2 = TextNode("This is a text node", TextType.LINK, "test")
        self.assertEqual(node, node2)
    def test_empty_link(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()