import os, json, datetime
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs, unquote_plus

ROOT = os.path.dirname(os.path.dirname(__file__))  # project root (folder above backend/)
TEMPLATE_PATH = os.path.join(ROOT, "frontend", "templates", "index.html")
STATIC_DIR = os.path.join(ROOT, "frontend", "static")
DATA_DIR = os.path.join(ROOT, "data")
DATA_FILE = os.path.join(DATA_DIR, "posts.json")

# ensure data dir and file
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([
            {"author": "system", "content": "welcome to leave message here!", "time": datetime.datetime.utcnow().isoformat()+"Z"}
        ], f, ensure_ascii=False, indent=2)

def load_posts():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_post(post):
    posts = load_posts()
    posts.insert(0, post)  # newest first
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def serve_static(path):
    # path starts with /static/
    rel = path[len("/static/"):]
    fs_path = os.path.join(STATIC_DIR, rel)
    if not os.path.isfile(fs_path):
        return None, None
    # set content type
    if fs_path.endswith(".css"):
        ctype = "text/css; charset=utf-8"
    elif fs_path.endswith(".js"):
        ctype = "application/javascript; charset=utf-8"
    else:
        ctype = "application/octet-stream"
    with open(fs_path, "rb") as f:
        return f.read(), ctype

def render_index():
    # read template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        tpl = f.read()
    posts = load_posts()
    # Build posts HTML (VULNERABLE: raw insertion without escaping)
    posts_html_parts = []
    for p in posts:
        author = p.get("author", "anonymous")
        time = p.get("time", "")
        content = p.get("content", "")
        posts_html_parts.append(
            f"<div class='post'><div class='meta'><strong>{author}</strong> <span class='time'>{time}</span></div>"
            f"<div class='content'>{content}</div></div><hr/>"
        )
    posts_html = "\n".join(posts_html_parts)
    # Replace placeholder {{posts}} in template
    page = tpl.replace("{{posts}}", posts_html)
    return page.encode("utf-8")

def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")

    # serve static files
    if path.startswith("/static/"):
        data, ctype = serve_static(path)
        if data is None:
            start_response("404 Not Found", [("Content-Type","text/plain")])
            return [b"Not Found"]
        start_response("200 OK", [("Content-Type", ctype)])
        return [data]

    if path == "/" and method == "GET":
        body = render_index()
        start_response("200 OK", [("Content-Type","text/html; charset=utf-8")])
        return [body]

    if path == "/post" and method == "POST":
        try:
            size = int(environ.get("CONTENT_LENGTH") or 0)
        except:
            size = 0
        raw = environ["wsgi.input"].read(size).decode("utf-8")
        params = parse_qs(raw)
        # parse_qs returns lists
        author = params.get("author", ["anonymous"])[0]
        content = params.get("content", [""])[0]
        # parse_qs returns percent-decoded strings, but keep as-is to show XSS
        post = {
            "author": author,
            "content": content,
            "time": datetime.datetime.utcnow().isoformat() + "Z"
        }
        save_post(post)
        # redirect back to index
        start_response("303 See Other", [("Location", "/")])
        return [b""]

    # fallback
    start_response("404 Not Found", [("Content-Type","text/plain")])
    return [b"Not Found"]

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 8000
    print(f"Starting vulnerable server on http://{HOST}:{PORT} (CTRL+C to stop)")
    make_server(HOST, PORT, application).serve_forever()
