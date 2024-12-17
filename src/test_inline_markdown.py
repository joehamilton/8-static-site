import unittest

from inline_markdown import split_nodes_image,split_nodes_link,extract_markdown_images,extract_markdown_links,split_nodes_delimiter,text_to_textnodes
from textnode import TextNode,TextType


class TestInlineMarkdown(unittest.TestCase):

    def test__extract_link1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        func = extract_markdown_images(text)
        output = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        self.assertEqual(func, output)

    def test__extract_image1(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        func = extract_markdown_links(text)
        output = [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        self.assertEqual(func, output)

    def test_nodes_delimiter1(self):
        input_node = [
            TextNode("This is a *test second italic node*", text_type=TextType.TEXT),
            TextNode("**BOLD node** OK", text_type=TextType.TEXT),
            TextNode("**This is all bold node**", text_type=TextType.TEXT),
            TextNode("*This is all ITALIC node*", text_type=TextType.TEXT)
            ]
        func = split_nodes_delimiter(input_node,"**",text_type=TextType.BOLD)
        func2 = split_nodes_delimiter(func,"*",text_type=TextType.ITALIC)
        output = [
            TextNode("This is a ", text_type=TextType.TEXT),
            TextNode("test second italic node", text_type=TextType.ITALIC),
            TextNode("BOLD node", text_type=TextType.BOLD),
            TextNode(" OK", text_type=TextType.TEXT),
            TextNode("This is all bold node", text_type=TextType.BOLD),
            TextNode("This is all ITALIC node", text_type=TextType.ITALIC)
            ]
        self.assertEqual(func2, output)

    def test_image1(self):
        node = TextNode(
            "This is text with an image ![alter](https://www.boot.dev/image.jpg) and ![youtube logo](https://www.youtube.com/logo.gif)",
            TextType.TEXT,
        )
        func = split_nodes_image([node])
        output = [
            TextNode("This is text with an image ", text_type=TextType.TEXT), 
            TextNode("alter", text_type=TextType.IMAGE, url="https://www.boot.dev/image.jpg"), 
            TextNode(" and ", text_type=TextType.TEXT), 
            TextNode("youtube logo", text_type=TextType.IMAGE, url="https://www.youtube.com/logo.gif")]
        self.assertEqual(func, output)

    def test_image2(self):
        node = TextNode(
            "![alter](https://www.boot.dev/image.jpg)",
            TextType.TEXT,
        )
        func = split_nodes_image([node])
        output = [
            TextNode("alter", text_type=TextType.IMAGE, url="https://www.boot.dev/image.jpg")
            ]
        self.assertEqual(func, output)

    def test_image3(self):
        node = TextNode(
            "![boot image](https://www.boot.dev/image.jpg)![google](https://www.google.com/image.jpg) <- nice images",
            TextType.TEXT,
        )
        func = split_nodes_image([node])
        output = [
            TextNode("boot image", text_type=TextType.IMAGE, url="https://www.boot.dev/image.jpg"),
            TextNode("google", text_type=TextType.IMAGE, url="https://www.google.com/image.jpg"),
            TextNode(" <- nice images", text_type=TextType.TEXT)
            ]
        self.assertEqual(func, output)

    def test_url1(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        func = split_nodes_link([node])
        output = [
            TextNode("This is text with a link ", text_type=TextType.TEXT), 
            TextNode("to boot dev", text_type=TextType.LINK, url="https://www.boot.dev"), 
            TextNode(" and ", text_type=TextType.TEXT), 
            TextNode("to youtube", text_type=TextType.LINK, url="https://www.youtube.com/@bootdotdev")]
        self.assertEqual(func, output)

    def test__text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        func = text_to_textnodes(text)
        output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(func, output)


if __name__ == "__main__":
    unittest.main()
