from textnode import TextNode
from textnode import TextType

def main():
    # Dummy text, test textnode.py imports
    node = TextNode(
        "Read the documentation", TextType.LINK,
        "https://example.com",
    )
    print(node)

main()
