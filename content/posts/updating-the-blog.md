Title: Using Jupyter Notebooks to Blog with Pelican
Author: Rob Osterburg
Slug: using-jupyter-notebooks-to-blog-with-pelican
Date: 2019-05-15
Category: Tutorial
Tags: pelican, jupyter lab, github pages
Summary: Using Pelican to generate a blog from jupyter notebook files

## Jupyter Notebook Support

If you are just getting starting blogging with Pelican and Jupyter Notebooks, then you need to install a plugin to generate HTML from your `.ipynb` files.  To do this add the [pelican-ipynb](https://github.com/danielfrg/pelican-ipynb) plugin for Pelican by entering `git submodule add git://github.com/danielfrg/pelican-ipynb.git plugins/ipynb`.  Now you have added a submodule to your repository.

If you have an existing Pelican blog that uses Jupyter notebooks as content,and have cloned a fresh version of your blog.  Then you will need to re-initialize your `pelican-ipynb` submodule.  First, re-initialize it by entering `git submodule init` followed by `git submodule update --rebase --remote`.  

Make sure you have the following lines to `pelicanconf.py`:

```# adding support for jupyter notebooks
MARKUP = ("md", "ipynb")
PLUGIN_PATHS = ["./plugins"]
PLUGINS = ["ipynb.markup"]
IGNORE_FILES = [".ipynb_checkpoints"]
IPYNB_USE_METACELL = True
```

## Update Pelican Plugins

Pelican uses plugins to add capabilities for generating blog content.  I work with Jupyter notebook (ipynb) files and use them as the basis for some of my blog posts.  This requires a plugin to generate the HTML and CSS from the ipynb file.  Generating the content requires a plugin and posting it on GitHub requires that the plugin be installed as a git submodule.  Having a repository within another repository -- especially one you are maintaining --  is rather intimidating.  Surprisingly, it is not as bad as it sounds.  Below are the steps to install install the [pelican-ipynb](https://github.com/danielfrg/pelican-ipynb) plugin for posting to Github pages.

1. Run `git submodule add git://github.com/danielfrg/pelican-ipynb.git plugins/ipynb`
2. Run `git submodule init`
3. Run `git submodule update` which downloads the latest version of pelican-ipynb into your `./plugins/ipynb` directory.

## Preparing your Post

1. Pelican uses metadata from your post to generate the post including the title, category, date, etc.  The [pelican-ipynb](https://github.com/danielfrg/pelican-ipynb) plugin offers several choices on how to do this.  I am choosing to add a cell to my notebook file and add the metadata there.  To do so you need to add a line with `IPYNB_USE_METACELL = True` to your `pelicanconf.py` file in the root directory of your blog.
2. Add the meta data from your blog post in a markdown cell containing the following tags:

    ```text
    Title:
    Slug:
    Date:
    Category:
    Tags:
    Author:
    Summary:
    ```

Now you are ready to generate blog posts from your Jupyter notebooks.

## Generating and Reviewing Content

1. Run `pelican content` from your blogs root directory and automatically detects changes in content
2. Fix any warnings or errors that Pelican reports  
3. `cd output` and open `http://localhost:8000` in your browser and review your blogs appearance
4. Start Python's build-in web server by running: `python -m http.server 8000`
5. Keep editing and refreshing to see your latest changes
6. Control-c to halt `pelican content`

## Publishing to Github Pages

1. Check in your changes to your `source` branch
2. Run `pelican content -o output -s pelicanconf.py`
3. Run `ghp-import output -b gh-pages`
4. Run `git push git@github.com:robocity.github.io.git gh-pages:master`

## Resources

1. [Documentation: Pelican Stable](https://docs.getpelican.com/en/stable/index.html)
2. [Repository: pelican-ipynb plugin]([pelican-ipynb](https://github.com/danielfrg/pelican-ipynb))
3. [Blog: Matt Makai's Excellent Pelican Posts](https://www.fullstackpython.com/pelican.html)
4. [Blog: Some Tips for Using Jupyter Notebooks with Pelican](https://pmbaumgartner.github.io/blog/jupyter-notebooks-for-pelican/)
5. [Blog: Hacking my way to a Jupyter notebook powered blog](https://nipunbatra.github.io/blog/2017/Jupyter-powered-blog.html)
