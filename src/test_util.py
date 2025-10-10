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

    def test_node_splitting_1(self):
        node_list = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        expected_result = [
                           TextNode("This is text with a ", TextType.TEXT),
                           TextNode("code block", TextType.CODE),
                           TextNode(" word", TextType.TEXT)
                           ]
        split_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        self.assertEqual(split_nodes, expected_result) 

    def test_node_splitting_2(self):
        node_list = [TextNode("This is text with a `code block` word and another `code crab` test", TextType.TEXT)]
        expected_result = [
                           TextNode("This is text with a ", TextType.TEXT),
                           TextNode("code block", TextType.CODE),
                           TextNode(" word and another ", TextType.TEXT),
                           TextNode("code crab", TextType.CODE),
                           TextNode(" test", TextType.TEXT)
                           ]
        split_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        self.assertEqual(split_nodes, expected_result) 

    def test_extract_markdown_images_1(self):
        input_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        actual_result = extract_markdown_images(input_text)
        self.assertEqual(expected_result, actual_result)

    def test_extract_markdown_link_1(self):
        input_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        actual_result = extract_markdown_links(input_text)
        self.assertEqual(expected_result, actual_result)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_2(self):
        node = TextNode(
            " ![image](https://i.imgur.com/zjjcJKZ.png) ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_3(self):
        node = TextNode(
            "This is a text node with no images.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text node with no images.", TextType.TEXT)
            ],
            new_nodes,
        )
    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertListEqual(result, expected)

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertListEqual(result, expected)

    def test_text_to_textnodes_italic(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertListEqual(result, expected)

    def test_text_to_textnodes_code(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertListEqual(result, expected)

    def test_text_to_textnodes_image(self):
        text = "This is an ![image](https://example.com/img.png) here"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertListEqual(result, expected)

    def test_text_to_textnodes_link(self):
        text = "This is a [link](https://example.com) here"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertListEqual(result, expected)

    def test_text_to_textnodes_multiple_types(self):
        text = "This is **bold** and _italic_ and `code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT)
        ]
        self.assertListEqual(result, expected)

    def test_text_to_textnodes_complex(self):
        text = "Text with **bold** and ![image](https://img.com/pic.png) and [link](https://site.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://img.com/pic.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://site.com")
        ]
        self.assertListEqual(result, expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_basic(self):
        md = "Block 1\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_with_whitespace(self):
        md = "  Block 1  \n\n  Block 2  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_single_block(self):
        md = "Just one block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block"])

    def test_markdown_to_blocks_multiline_in_block(self):
        md = "Block 1\nLine 2 of block 1\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1\nLine 2 of block 1", "Block 2"])

    def test_markdown_to_blocks_empty_blocks(self):
        md = "Block 1\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        # Should skip completely empty blocks
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = "\n\nBlock 1\n\nBlock 2\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_three_blocks(self):
        md = "First\n\nSecond\n\nThird"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First", "Second", "Third"])

    def test_markdown_to_blocks_complex(self):
        md = """# Heading

Paragraph with multiple
lines of text

- List item 1
- List item 2

Another paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "# Heading",
            "Paragraph with multiple\nlines of text",
            "- List item 1\n- List item 2",
            "Another paragraph"
        ])
if __name__ == "__main__":
    unittest.main()
