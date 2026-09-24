import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is italic test text node", TextType.ITALIC)
        node4 = TextNode("This is italic test text node", TextType.ITALIC)
        self.assertEqual(node3, node4)

        node5 = TextNode("This is 'CODE' test text node", TextType.CODE)
        node6 = TextNode("This is 'CODE' test text node", TextType.CODE)
        self.assertEqual(node5, node6)

        node = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is italic test text node", TextType.ITALIC)
        self.assertNotEqual(node, node4)

if __name__ == "__main__":
    unittest.main()