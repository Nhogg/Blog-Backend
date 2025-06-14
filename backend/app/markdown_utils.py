"""
markdown_utils.py
    Define methods for converting markdown to HTML.
"""

# Imports
import markdown2

def convert_markdown_to_html(markdown: str) -> str:
    return markdown2.markdown(markdown)