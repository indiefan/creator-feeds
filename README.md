FastAPI-based server for generating creator-based rss feeds via configuration-driven web-scraping

# Configuration
Uses nested [ConfigObj](https://configobj.readthedocs.io/en/latest/configobj.html) format to configure creator feeds parsing. Top-level sections are expected to be creator identifiers specified as valid url parts (e.g. names with spaces converted to underscores).

Creator sections are comprised of one or more feed configs. A feed config requires a `url` (this is the content that will be scrapped for items) and an `item` section which describes how to build each feed item.

Item sections require a `selector`, which is a CSS selector string compatible with [BeautifulSoup](https://pypi.org/project/beautifulsoup4/), and a `selectors` section.

Selectors sections are a collection of arbitrary named CSS selector strings that will be parsed for each item.

`title`, `link`, and `date` are required to be specified, either directly as selectors, or else as [Genshi](https://genshi.edgewall.org/wiki/Documentation/0.6.x/templates.html#python-api) templated strings in the Item Section. The text and attributes from all selectors are available to the templates.

e.g. 
```
[Ian_Cohen]
	[[Pitchfork Album Reviews]]
	url = https://pitchfork.com/staff/ian-cohen/albumreviews/
		[[[item]]]
		selector = .result-item
		timezone = America/Los_Angeles
		title = ${band} - ${album}
		link = https://pitchfork.com${short_link_attrs.href}
			[[[[selectors]]]]
			band = .review .review__title-artist > li
			album = .review .review__title-album > em
			short_link = .review > a
			date = .pub-date

	[[Uproxx Articles]]
	url = https://uproxx.com/author/ian-cohen/
		[[[item]]]
		selector = .grid-area .grid-item
		timezone = America/Los_Angeles
			[[[[selectors]]]]
			title = .entry-title > a
			link = .entry-title > a
			date = .published
```

# Local Development
To start the server locally, first install the requirements (preferably in a virtualenv) with `pip install requirements.txt` then run the startup script _from the app directory_ (running it from elsewhere would require modulization that's incompatible with the docker deployment method).

`cd app && ./startup`

The app should now be accessible e.g.

`http://localhost:8000/creator/Ian_Cohen` and
`http://localhost:8000/feed/Ian_Cohen.rss.xml`

# Deployment
A basic Dockerfile is included for containerization, and the `deploy` script exists for deploying to the same machine as development, and by default binds to port 8080 instead.

