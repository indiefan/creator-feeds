from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse

from creatorfeed import CreatorFeed

app = FastAPI()

@app.get("/feed/{creator}.rss.xml")
def creator_feed(creator: str):
    feed = CreatorFeed(creator)
    return Response(feed.get_feed(), media_type="application/xml")

@app.get("/creator/{creator}")
def creator_page(creator: str):
    html = f'<html><head><link rel="alternate" type="application/rss+xml" href="http://indiefan.duckdns.org:8000/feed/{creator}.rss.xml" title="Creator Feed" /></head><body>Creator Feed</body></html>'
    return HTMLResponse(html)

