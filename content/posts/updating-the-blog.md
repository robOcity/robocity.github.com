Title: Using Jupyter Notebooks to Blog with Pelican
Author: Rob Osterburg
Slug: using-jupyter-notebooks-to-blog-with-pelican
Date: 2019-05-15
Category: Tutorial
Tags: pelican, jupyter lab, github pages
Summary: Using Pelican to generate a blog from Jupyter notebook files

## Jupyter Notebook Support

If you are just getting starting blogging with Pelican and Jupyter Notebooks, then you need to install a plugin to generate HTML from your `.ipynb` files.  To do this add the [pelican-ipynb](https://github.com/danielfrg/pelican-ipynb) plugin for Pelican by entering `git submodule add git://github.com/danielfrg/pelican-ipynb.git plugins/ipynb`.  Now you have added a submodule to your repository.

If you have an existing Pelican blog that uses Jupyter notebooks as content,and have cloned a fresh version of your blog.  Then you will need to re-initialize your `pelican-ipynb` submodule.  First, re-initialize it by entering `git submodule init` followed by `git submodule update --rebase --remote`.  

Make sure you have the following lines to `pelicanconf.py`:

```# adding support for jupyter notebooks
# see: https://www.scribd.com/document/359497520/Building-a-Data-Science-Portfolio-Making-a-Data-Science-Blog
MARKUP = ("md", "ipynb")
PLUGIN_PATHS = ["./plugins"]
PLUGINS = ["ipynb.markup"]
IGNORE_FILES = [".ipynb_checkpoints"]
IPYNB_USE_METACELL = True
```

Now you are ready to generate blog posts from your Jupyter notebooks. 

## Generating Content

1. 

## Github Pages



## Resources

1. [Matt Makai's Excellent Pelican Posts](https://www.fullstackpython.com/pelican.html)
2. [pelican-ipynb plugin]([pelican-ipynb](https://github.com/danielfrg/pelican-ipynb))