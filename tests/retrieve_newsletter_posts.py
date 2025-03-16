from substack_api import Newsletter

# Initialize a newsletter by its URL
newsletter = Newsletter("https://example.substack.com")

# Get recent posts (returns Post objects)
recent_posts = newsletter.get_posts(limit=5)

# Print the response
print(recent_posts)
