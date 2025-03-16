import os
import re
from dotenv import load_dotenv
from substack_api import Newsletter, Post
import html2text

# Load environment variables from .env (ensure this file is not committed to your repo)
load_dotenv()

# Retrieve environment variables (use placeholders in your repo; actual values in your local .env file)
subdomain = os.getenv("USER_SUBSTACK_SUBDOMAIN")  # e.g., "your_subdomain"
if not subdomain:
    raise ValueError("USER_SUBSTACK_SUBDOMAIN is not set in the environment variables.")

obsidian_path = os.getenv("OBSIDIAN_DESTINATION_PATH")  # e.g., "/path/to/your/obsidian/vault"
if not obsidian_path:
    raise ValueError("OBSIDIAN_DESTINATION_PATH is not set in the environment variables.")

def extract_title_from_url(url):
    """
    Extract a human-friendly title from a Substack post URL.
    
    Example:
      Input: "https://example.substack.com/p/daily-posts-experiment-pt-2"
      Output (fallback): "Daily Posts Experiment Pt 2"
    """
    parts = url.split('/p/')
    if len(parts) > 1:
        slug = parts[1].strip('/')
        title = slug.replace('-', ' ').title()
        return title
    return url  # fallback if format is unexpected

def safe_filename_from_title(title):
    """
    Returns a safe filename by removing characters not allowed in filenames,
    but keeps the proper casing and spacing.
    """
    # Remove any of these illegal characters: <>:"/\|?*
    return re.sub(r'[<>:"/\\|?*]', '', title)

# Construct your newsletter URL using the subdomain
newsletter_url = f"https://{subdomain}.substack.com"
newsletter = Newsletter(newsletter_url)

# Retrieve posts (adjust the limit if needed)
posts = newsletter.get_posts(limit=100)

# Set up the HTML to Markdown converter
converter = html2text.HTML2Text()
converter.ignore_links = False  # Keep links in the Markdown
converter.body_width = 0        # Avoid line wrapping

# Process each post and write to the Obsidian vault (overwrites existing files)
for post_obj in posts:
    # Initialize the post and get its metadata
    post = Post(post_obj.url)
    metadata = post.get_metadata()
    
    # Use metadata title if available; otherwise, fall back to the URL-derived title
    title = metadata.get("title") or extract_title_from_url(post_obj.url)
    
    # Generate a safe filename from the title while preserving casing and spaces
    file_name = f"{safe_filename_from_title(title)}.md"
    file_path = os.path.join(obsidian_path, file_name)
    
    # Convert the post's HTML content to Markdown
    html_content = post.get_content()
    markdown_content = converter.handle(html_content)
    
    # Build the Markdown file content with the title as a header
    file_content = f"# {title}\n\n" + markdown_content
    
    # Write the content to the file (overwriting if the file exists)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    print(f"Saved '{title}' to {file_path}")

