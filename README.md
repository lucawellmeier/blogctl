# octoblog

This project aims to be a very simple and straightforward GitHub Pages command-line blogging tool.
The goal is to emulate the behavior of an actual dynamic blog (on both the blogger and reader 
side) on the static Github Pages hosting.

Features:
 - full control through a simple **command-line interface**
 - wraps around Git to serve your personal blog through the free **GitHub pages** service
 - post articles written in **Markdown**
 - automatic tracking of **publishing and change dates** through the underlying Git repo
 - flexible theme design with **Jinja2 templating**
 - automatic creation of **collections** by category and months (similar to Wordpress archives)

## Setup

**Note:** The tool is currently only tested on Linux. Due to heavy usage of Linux-style paths
I doubt that it will be usable on Windows as-is, but support will be probably added in the future.
If you are interested in Windows support you can create an issue to increase priority.

Requirements:
 - git
 - a personal GitHub account
 - Python 3.8
 - libraries `markdown2` and `jinja2` (installable via `pip`)

Make sure you have a working GitHub pages repo (just create a new GitHub repository named
`<YOUR USERNAME>.github.io`) and that it is cleared to avoid possible file conflicts.

After cloning the `octoblog` repo, you can run the tool through
```
python /path/to/cloned-repo/octoblog.py [ARGUMENTS].
```
However, I prefer to make it executable and create a symlink to `octoblog.py` somewhere in
my `PATH`. Thus, in the following I instead use:
```
octoblog [ARGUMENTS]
```

Next, create a directory which shall contain the blog data and config and run:
```
mkdir myblog
cd myblog
octoblog init <REMOTE URL>
```
`<REMOTE URL>` is the URL of the GitHub repository (should be ending in `.git`).
This will create the basic file structure containing an articles and pages and the
default theme.

If you want to restore an existing *octoblog* run `octoblog clone <REMOTE URL>`.

Finally, Open `config.json` in a text editor and correct the field `url` by inserting your 
GitHub username.
*octoblog* is now set up and you are ready to spread your word.

## Usage

The basic directory structures looks like this:
```
myblog/
	config.json
	articles/
		welcome.md
		italian/
			buongiorno.md
	pages/
		about.md
	assets/
		example.png
	themes/
		plain/
			...
```

We go through all the components' purposes by example.

### Posting articles

We want to post two articles, `hello.md` and `ciao.md`, say, with contents
```
-- hello.md
\# Hello there
How are you?

-- ciao.md
\# Hallo Freundchen
Wie geht's?
```
Put `hello.md` into `articles/` and then run `octoblog preview`. The tool will freshly build
the whole blog and put it into `.cache/preview/`. Open the `index.html` file in there in your
browser to view the result.

The first Markdown header will be the article title and the first paragraph its short description.

Note that both new articles have an "Invalid Date" message instead of a publishing date. 
This changes as soon as we run `octoblog publish`. All your changes will be online a few moments 
after that and can be found on your GitHub Pages URL.

## Customizing your theme

