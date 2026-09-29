import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
	def test_eq_bold_nodes(self):
		# Testing for equality of two bold nodes.
		node1 = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node1, node2)

	def test_eq_italic_nodes(self):
		# Testing for equality of two italic nodes.
		node3 = TextNode("This is a text node", TextType.ITALIC)
		node4 = TextNode("This is a text node", TextType.ITALIC)
		self.assertEqual(node3, node4)

	def test_eq_different_types(self):
		# Testing for inequality of nodes with different types. 
		node5 = TextNode("This is a text node", TextType.BOLD)
		node6 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node5, node6)

	def test_eq_code_nodes(self):
		# Testing for equality of two code nodes.
		node7 = TextNode("This is a text node", TextType.CODE)
		node8 = TextNode("This is a text node", TextType.CODE)
		self.assertEqual(node7, node8)

	def test_eq_link_nodes(self):
		# Testing for equality of two link nodes.
		node9 = TextNode("This is a text node", TextType.LINK)
		node10 = TextNode("This is a text node", TextType.LINK)
		self.assertEqual(node9, node10)

	def test_eq_image_nodes(self):
		# Testing for equality of two image nodes.
		node11 = TextNode("This is a text node", TextType.IMAGE)
		node12 = TextNode("This is a text node", TextType.IMAGE)
		self.assertEqual(node11, node12)

	def test_eq_url_nodes(self):
		# Testing for equality of two url nodes.
		node13 = TextNode("Click here", TextType.LINK, "https://example.com")
		node14 = TextNode("Click here", TextType.LINK, "https://example.com")
		self.assertEqual(node13, node14)

	def test_not_eq_url_nodes(self):
		# Testing for inequality of two url nodes.
		node15 = TextNode("Click here", TextType.LINK, "https://example.com")
		node16 = TextNode("Click here", TextType.LINK, "https://different.com")
		self.assertNotEqual(node15, node16)

	def test_not_eq_with_missing_url(self):
		# Testing for inequality of nodes wih one URl and one withou.
		node17 = TextNode("Click here", TextType.LINK, "https://example.com")
		node18 = TextNode("Click here", TextType.LINK) # No URL.
		self.assertNotEqual(node17, node18)

	def test_not_eq_different_text(self):
		# Testing for inequality of two nodes with different text.
		node19 = TextNode("This is a text node", TextType.ITALIC)
		node20 = TextNode("This is a different text node", TextType.ITALIC)
		self.assertNotEqual(node19, node20)

class TestTextNodeToHTMLNode(unittest.TestCase):
    	def test_text(self):
        	node = TextNode("This is a text node", TextType.TEXT)
        	html_node = text_node_to_html_node(node)
        	self.assertEqual(html_node.tag, None)
        	self.assertEqual(html_node.value, "This is a text node")

    	def test_image(self):
        	node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        	html_node = text_node_to_html_node(node)
        	self.assertEqual(html_node.tag, "img")
        	self.assertEqual(html_node.value, "")
        	self.assertEqual(
        	    html_node.props,
        	    {"src": "https://www.boot.dev", "alt": "This is an image"},
        	)

    	def test_bold(self):
        	node = TextNode("This is bold", TextType.BOLD)
        	html_node = text_node_to_html_node(node)
        	self.assertEqual(html_node.tag, "b")
        	self.assertEqual(html_node.value, "This is bold")


if __name__ == "__main__":
    unittest.main()
