import requests
import datetime
import base64
import random
import json
import os

# ==== CONFIG ====
SITE_URL = "https://getomnirecall.com"
POSTS_URL = f"{SITE_URL}/wp-json/wp/v2/posts"
MEDIA_URL = f"{SITE_URL}/wp-json/wp/v2/media"

USERNAME = "qrs0u"
APP_PASSWORD = "suUb YmmU qH9O WIMK 92Ow 5kyM"

AUTH = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()

HEADERS = {
    "Authorization": f"Basic {AUTH}"
}

TOPIC_FILE = "used_topics.json"

# ==== LOAD/SAVE TOPICS ====
def load_used():
    if os.path.exists(TOPIC_FILE):
        return set(json.load(open(TOPIC_FILE)))
    return set()

def save_topic(topic):
    used = load_used()
    used.add(topic)
    json.dump(list(used), open(TOPIC_FILE, "w"))

# ==== TREND ENGINE ====
TRENDS = [
    "Agentic AI systems",
    "AI memory systems",
    "AI productivity",
    "AI automation workflows",
    "AI operating systems",
    "AI knowledge graphs",
    "AI orchestration platforms"
]

ANGLES = [
    "in 2026",
    "for startups",
    "real-world use cases",
    "what most companies get wrong",
    "future predictions",
    "complete guide"
]

HOOKS = ["Why", "How", "The Future of", "Inside"]

def generate_topic():
    used = load_used()

    while True:
        topic = f"{random.choice(HOOKS)} {random.choice(TRENDS)} {random.choice(ANGLES)}"
        if topic not in used:
            save_topic(topic)
            return topic

# ==== INTERNAL LINKS ====
INTERNAL_LINKS = {
    "AI memory systems": "https://getomnirecall.com",
    "OmniSuite Pro": "https://getomnirecall.com"
}

def add_links(content):
    for k, v in INTERNAL_LINKS.items():
        if k in content:
            content = content.replace(k, f'<a href="{v}">{k}</a>', 1)
    return content

# ==== BLOG GENERATOR ====
def generate_blog():
    title = generate_topic()

    content = f"""
    <h2>{title}</h2>

    <p>{title} is shaping the next generation of intelligent systems where software evolves into autonomous execution layers.</p>

    <h2>What’s Happening</h2>
    <p>AI is shifting from passive tools into active systems capable of decision-making and contextual understanding.</p>

    <h2>Why It Matters</h2>
    <p>Businesses adopting these systems gain speed, efficiency, and competitive advantage.</p>

    <h2>OmniSuite Pro Advantage</h2>
    <p>OmniSuite Pro connects memory, automation, and intelligence into one unified platform.</p>
    """

    content = add_links(content)

    return title, content

# ==== IMAGE ====
IMAGE_URL = "https://galaxy-prod.tlcdn.com/preview/image/chat/user_38S2dp9mpLtWywQMenmelAajXPB/7aeb9b7b-7549-4bff-8fd0-13d690285bce.png"

def upload_image():
    img = requests.get(IMAGE_URL).content

    headers = HEADERS.copy()
    headers.update({
        "Content-Disposition": "attachment; filename=blog.jpg",
        "Content-Type": "image/jpeg"
    })

    res = requests.post(MEDIA_URL, headers=headers, data=img)
    return res.json()["id"]

# ==== CREATE POST ====
def create_post(title, content, image_id, days):
    date = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat()

    post = {
        "title": title,
        "content": content,
        "status": "future",
        "featured_media": image_id,
        "date": date
    }

    res = requests.post(POSTS_URL, headers=HEADERS, json=post)
    return res.json()

# ==== RUN ====
if __name__ == "__main__":
    image_id = upload_image()

    for i in range(1, 30):  # 30 scheduled posts
        title, content = generate_blog()
        post = create_post(title, content, image_id, i)
        print("Scheduled:", post.get("link", "error"))