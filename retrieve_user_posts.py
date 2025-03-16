import os
from dotenv import load_dotenv
from substack_api import Newsletter, Post
import html2text

# Load environment variables from .env
load_dotenv()

# Get your subdomain from the environment variable
subdomain = os.getenv("USER_SUBSTACK_SUBDOMAIN")
if not subdomain:
    raise ValueError("USER_SUBSTACK_SUBDOMAIN is not set in the environment variables.")

# Construct your newsletter URL
newsletter_url = f"https://{subdomain}.substack.com"

# Initialize the newsletter
newsletter = Newsletter(newsletter_url)

# Retrieve all posts (adjust the limit if needed)
posts = newsletter.get_posts(limit=100)

# Create an HTML to Markdown converter
converter = html2text.HTML2Text()
converter.ignore_links = False  # Include links in the Markdown
converter.body_width = 0        # Prevent line wrapping

# For each post, convert the HTML content to Markdown and print it
for post_obj in posts:
    post = Post(post_obj.url)
    html_content = post.get_content()
    markdown_content = converter.handle(html_content)
    
    print(f"## Post URL: {post_obj.url}\n")
    print(markdown_content)
    print("\n---\n")

