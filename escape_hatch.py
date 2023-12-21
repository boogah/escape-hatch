import os
import json
import markdownify
from datetime import datetime
from collections import defaultdict

def export_posts_to_markdown(base_folder):
    posts = []

    for root, dirs, files in os.walk(base_folder):
        for file_name in files:
            if file_name.endswith('.likes.json'):
                continue  # Skip files ending with .likes.json

            file_path = os.path.join(root, file_name)
            with open(file_path, 'r') as file:
                post = json.load(file)
                posts.append(post)

    # Sort posts by the 'published' date
    posts.sort(key=lambda x: x.get('published', ''))

    # Group posts by month and year
    grouped_posts = defaultdict(list)
    for post in posts:
        published = post.get('published', '')
        if published:
            month_year = datetime.fromisoformat(published.rstrip("Z")).strftime("%B %Y")
            grouped_posts[month_year].append(post)

    markdown_output = ""
    # Check if there are any posts to determine the author
    if posts:
        # Extract and format the 'attributedTo' field as 'username@domain'
        first_post = posts[0]
        attributed_to_url = first_post.get('attributedTo', '')
        if attributed_to_url:
            parts = attributed_to_url.split('/')
            username = parts[-1] if len(parts) > 1 else ""
            domain = parts[2] if len(parts) > 2 else ""
            attributed_to = f"{username}@{domain}"
        else:
            attributed_to = "Unknown User"
        markdown_output += f"# Posts from {attributed_to}\n\n\n"

    for month_year, posts in grouped_posts.items():
        markdown_output += f"## {month_year}\n\n"  # Month-Year header

        for post in posts:
            # Convert HTML content to Markdown and strip trailing newlines
            content = markdownify.markdownify(post.get('content', '')).rstrip('\n')
            published = post.get('published', '')

            # Convert and format the 'published' date
            if published:
                published_datetime = datetime.fromisoformat(published.rstrip("Z"))
                formatted_published = published_datetime.strftime("%m-%d-%y %H:%M:%S")
            else:
                formatted_published = "Unknown Date"

            # Format and add the post to the markdown output with proper newlines
            markdown_output += f"\n{content}\n\n"  # Ensure two newlines after the content
            markdown_output += f"**Published:** {formatted_published}\n\n"

    return markdown_output

# Example usage of the function
base_folder = 'app/.data/posts/'

markdown_content = export_posts_to_markdown(base_folder)
print(markdown_content)  # This should print the markdown content
