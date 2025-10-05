from textnode import TextType, TextNode


def main():
    textNode = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(repr(textNode))

main()