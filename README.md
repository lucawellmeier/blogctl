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
I dought that it will be usable on Windows as-is, but support will be probably be added soon.
If you are interested in Windows support you can create an issue to increase priority.

Requirements:
 - git
 - a personal GitHub account
 - Python 3.8
 - libraries `markdown2` and `jinja2` (installable via `pip`)

Make sure you have a working GitHub pages repo (just create a new GitHub repository named
`<YOUR USERNAME>.github.io`) and backup and clear it to avoid possible file conflicts.

After cloning the `octoblog` repo, you can run the tool through
```
python /path/to/cloned-repo/octoblog.py [ARGUMENTS].
```
However, I prefer to make it executable and create a symlink to `octoblog.py` somewhere in
my `PATH`. Thus, in the following I instead use:
```
octoblog [ARGUMENTS]
```

Next, create a directory which shall contain the blog and run:
```
mkdir myblog
cd myblog
octoblog init <REMOTE URL>
```
`<REMOTE URL>` is the URL of the GitHub repository (should be ending in `.git`)
This will create the basic file structure containing an example article page and the
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

All posts go to `articles`. You can create sub-directories in there to categorize
your articles. The default category name will be the directory name but it can be altered
in the config file under `category_titles`.

Be aware that in article listings the first header and the first paragraph will be used as article 
title and description, respectively.

Static pages go to `pages`. These can be accessed in the `menu` field of the config file or through
a query function (see below).

Images, documents, ... go to `assets`. Inside markdown the url of this folder can be accessed 
through the Jinja2 global variable `ASSETS` (`{{ASSETS}}/example.png`, for example).

## Customizing your theme

