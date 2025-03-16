from substack_api import Post

# Initialize a post by its URL
post = Post("https://example.substack.com/p/heroes-who-came-to-look-for-example")

# Get post metadata
metadata = post.get_metadata()

# Get the post's HTML content
content = post.get_content()

print(content)
