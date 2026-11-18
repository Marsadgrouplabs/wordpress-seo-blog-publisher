#!/usr/bin/env python
"""WordPress REST helper for the wordpress-seo-blog-publisher skill.

Reads site logins from ~/.wp-publisher/sites.txt, or the file named by WP_SITES_FILE
(3 lines per site: url, user, application password; blank line between sites).
Never prints passwords.
Uses only the Python standard library.

Usage:  python wp.py <command> <site> [options]
  sites                                  list configured sites
  check <site>                           verify login + show role
  posts <site> [--n 30] [--status publish]   list posts (id, slug, link, title) - for internal-link checks
  ensure-category <site> "Name"          find or create a category, prints its id
  ensure-tags <site> "a,b,c"             find or create tags, prints comma-separated ids
  upload <site> <file> [--alt TEXT] [--title TEXT]   upload an image, prints id + url
  draft <site> --title T --content-file F [--slug S] [--excerpt E] [--category ID] [--tags 1,2] [--featured ID]
  update <site> <post_id> [same options as draft]    change an existing post
  publish <site> <post_id>               set status to publish
  get <site> <post_id>                   show status, link, title
<site> is any part of the site URL, e.g. example or blog.example.com
"""
import sys, os, json, mimetypes, uuid, argparse, html
import urllib.request, urllib.error, urllib.parse, base64

# A normal browser User-Agent: the hosts' ModSecurity blocks the default python/curl one (HTTP 406).
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def die(msg, code=1):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(code)


def load_sites():
    default = os.path.join(os.path.expanduser("~"), ".wp-publisher", "sites.txt")
    path = os.path.expanduser(os.environ.get("WP_SITES_FILE") or default)
    if not os.path.exists(path):
        die("sites.txt not found at %s. Create it from scripts/sites.example.txt" % path)
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f.read().replace("\r", "").split("\n") if l.strip()]
    sites = []
    for i in range(0, len(lines) - 2, 3):
        sites.append({"url": lines[i].rstrip("/"), "user": lines[i + 1], "pass": lines[i + 2]})
    return sites


def pick_site(name):
    sites = load_sites()
    n = name.lower().replace("https://", "").replace("http://", "").strip("/")
    exact = [s for s in sites if s["url"].lower().replace("https://", "").replace("http://", "") == n]
    if exact:
        return exact[0]
    hits = [s for s in sites if n in s["url"].lower()]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        die("no site matches '%s'. Run: python wp.py sites" % name)
    die("'%s' matches several sites: %s. Be more specific." % (name, ", ".join(s["url"] for s in hits)))


def call(site, method, path, body=None, raw=None, content_type=None):
    url = site["url"] + "/wp-json/wp/v2" + path
    token = base64.b64encode(("%s:%s" % (site["user"], site["pass"])).encode("utf-8")).decode()
    headers = {"User-Agent": UA, "Accept": "application/json", "Authorization": "Basic " + token}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif raw is not None:
        data = raw
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", "replace")
        if e.code == 406:
            die("HTTP 406 - blocked by the host's ModSecurity firewall (not WordPress). Ask the host to allow /wp-json/.")
        try:
            j = json.loads(txt)
            die("HTTP %s %s: %s" % (e.code, j.get("code"), j.get("message")))
        except ValueError:
            die("HTTP %s: %s" % (e.code, txt[:200]))
    except urllib.error.URLError as e:
        die("cannot reach %s: %s" % (site["url"], e.reason))


def multipart(fields, file_field, file_path):
    b = uuid.uuid4().hex
    out = []
    for k, v in fields.items():
        if v:
            out.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n" % (b, k, v)).encode("utf-8"))
    ctype = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    fname = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        content = f.read()
    out.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\nContent-Type: %s\r\n\r\n"
                % (b, file_field, fname, ctype)).encode("utf-8"))
    out.append(content)
    out.append(("\r\n--%s--\r\n" % b).encode("utf-8"))
    return b"".join(out), "multipart/form-data; boundary=" + b


def find_or_create(site, kind, name):
    found = call(site, "GET", "/%s?search=%s&per_page=100&_fields=id,name" % (kind, urllib.parse.quote(name)))
    for item in found:
        if html.unescape(item["name"]).strip().lower() == name.strip().lower():
            return item["id"], False
    return call(site, "POST", "/" + kind, body={"name": name})["id"], True


def build_post_body(a):
    body = {}
    if a.title is not None:
        body["title"] = a.title
    if a.content_file:
        with open(a.content_file, encoding="utf-8-sig") as f:
            body["content"] = f.read()
    if a.slug:
        body["slug"] = a.slug
    if a.excerpt is not None:
        body["excerpt"] = a.excerpt
    if a.category:
        body["categories"] = [int(x) for x in a.category.split(",") if x]
    if a.tags:
        body["tags"] = [int(x) for x in a.tags.split(",") if x]
    if a.featured:
        body["featured_media"] = int(a.featured)
    return body


def show_post(p):
    print("id: %s" % p["id"])
    print("status: %s" % p.get("status"))
    print("link: %s" % p.get("link"))
    title = p.get("title")
    if isinstance(title, dict):
        title = title.get("raw") or title.get("rendered")
    print("title: %s" % title)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "sites":
        for s in load_sites():
            print(s["url"])
        return

    p = argparse.ArgumentParser(prog="wp.py " + cmd)
    p.add_argument("site")
    p.add_argument("arg", nargs="?")
    p.add_argument("--n", type=int, default=30)
    p.add_argument("--status", default="publish")
    p.add_argument("--alt", default="")
    p.add_argument("--title")
    p.add_argument("--content-file")
    p.add_argument("--slug")
    p.add_argument("--excerpt")
    p.add_argument("--category")
    p.add_argument("--tags")
    p.add_argument("--featured")
    a = p.parse_args(sys.argv[2:])
    site = pick_site(a.site)

    if cmd == "check":
        me = call(site, "GET", "/users/me?context=edit&_fields=id,name,roles")
        print("%s OK - %s (%s)" % (site["url"], me.get("name"), ",".join(me.get("roles", []))))
    elif cmd == "posts":
        rows = call(site, "GET", "/posts?status=%s&per_page=%d&_fields=id,slug,link,title,date" % (a.status, a.n))
        for r in rows:
            print("%s | %s | %s | %s" % (r["id"], r["slug"], r["link"], html.unescape(r["title"]["rendered"])))
    elif cmd == "ensure-category":
        if not a.arg:
            die("category name required")
        i, created = find_or_create(site, "categories", a.arg)
        print(i, "(created)" if created else "(existing)")
    elif cmd == "ensure-tags":
        if not a.arg:
            die("tags required, comma-separated")
        ids = []
        for t in [x.strip() for x in a.arg.split(",") if x.strip()]:
            i, _ = find_or_create(site, "tags", t)
            ids.append(str(i))
        print(",".join(ids))
    elif cmd == "upload":
        if not a.arg or not os.path.exists(a.arg):
            die("image file not found: %s" % a.arg)
        title = a.title or os.path.splitext(os.path.basename(a.arg))[0]
        raw, ct = multipart({"title": title, "alt_text": a.alt}, "file", a.arg)
        m = call(site, "POST", "/media", raw=raw, content_type=ct)
        print("id: %s" % m["id"])
        print("url: %s" % m.get("source_url"))
    elif cmd == "draft":
        body = build_post_body(a)
        if "title" not in body or "content" not in body:
            die("--title and --content-file are required")
        body["status"] = "draft"
        show_post(call(site, "POST", "/posts", body=body))
    elif cmd == "update":
        if not a.arg:
            die("post id required")
        body = build_post_body(a)
        if not body:
            die("nothing to update")
        show_post(call(site, "POST", "/posts/%s" % a.arg, body=body))
    elif cmd == "publish":
        if not a.arg:
            die("post id required")
        show_post(call(site, "POST", "/posts/%s" % a.arg, body={"status": "publish"}))
    elif cmd == "get":
        if not a.arg:
            die("post id required")
        show_post(call(site, "GET", "/posts/%s?context=edit" % a.arg))
    else:
        die("unknown command '%s'. Run: python wp.py help" % cmd)


if __name__ == "__main__":
    main()
