import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_node_link(self):
        node = LeafNode(
            "a",
            "What a strange world",
            {"href":"https://google.com","class": "primary"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://google.com" class="primary">What a strange world</a>',
        )
    def test_leaf_node_strong(self):
        node = LeafNode(
            "strong",
            "THIS IS STRONG!",
        )
        self.assertEqual(
            node.to_html(),
            '<strong>THIS IS STRONG!</strong>',
        )
    def test_leaf_node_no_tag(self):
        node = LeafNode(
            None,
            "I like it raw.",
        )
        self.assertEqual(
            node.to_html(),
            'I like it raw.',
        )

    def test_leaf_node_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
        )
    def test_leaf_node_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("a", "Link text", {"href":"http://www.google.com"}),
                LeafNode("strong", "Bold text", {"class":"bold_style"}),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><a href="http://www.google.com">Link text</a><strong class="bold_style">Bold text</strong>Normal text</p>',
        )

if __name__ == "__main__":
    unittest.main()