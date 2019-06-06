Title: Using Jupyter Notebooks to Blog with Pelican
Author: Rob Osterburg
Slug: using-jupyter-notebooks-to-blog-with-pelican
Date: 2019-05-15
Category: Tutorial
Tags: pelican, jupyter, nbconvert, markdown, github pages
Summary: Using Pelican to generate a blog from jupyter notebook files

My blog relates to data science, software development and topics like bicycle safety that are close to my heart.  Minimizing any friction in my content creation workflow is important, so simplicity is a goal.  Here I share my experiences with you.  

## Generating Blog Posts from Jupyter Notebooks

Jupyter notebooks as a prime content source of data science content.  Why not use those for my blog posts?  Much of my exploratory work is captured in notebooks anyway, so I gave it go.  You can do this using `jupyter nbconvert` or installing a plugin in Pelican.  

Pelican uses plugins to generate HTML and CSS from Jupyter Notebooks.  [Pelican-ipynb](https://github.com/danielfrg/pelican-ipynb) has more than 300 stars on Github and seemed to fit the bill perfectly.  The link to the Github repo has good documentation and all the configuration details you need to get started.  It worked well on my local system but I had problems with having my blog posts published once uploaded to github.   The plugins are git submodules -- a repo in repo -- and I suspect how I handled them when pushing my output to the master branch may be part of the problem.  After several attempts and no success I moved on to nbconvert.

## Preparing your Post

1. Pelican uses metadata to tag and title your posts.  For markdown documents, you need to include these tags ascribing content to each.  If you are going with notebook based approach put these tags into a markdown cell.  

    ```text
    Title:
    Slug:
    Date:
    Category:
    Tags:
    Author:
    Summary:
    ```

Now you are ready to generate your blog.

## Generating and Reviewing Content

1. Run `pelican content` from your blogs root directory and automatically detects changes in content
2. Fix any warnings or errors that Pelican reports  
3. `cd output` and open `http://localhost:8000` in your browser and review your blogs appearance
4. Start Python's build-in web server by running: `python -m http.server 8000`
5. Keep editing and refreshing to see your latest changes
6. Control-c to halt `pelican content`

## Publishing to Github Pages

Github pages support individuals and organizations.  *For individuals like me, you have to publish your blog on the master branch of your pages repository.*  Instead being the ultimate source of blog, master is where your build artifacts reside.  Think generated HTML and CSS files.  I find this counter intuitive and I wrote this post to remind myself of this counter intuitive reality.  

1. Check in your changes to your `source` branch
2. Run `pelican content -o output -s pelicanconf.py`
3. Run `ghp-import output -b gh-pages`
4. Run `git push git@github.com:robocity.github.io.git gh-pages:master`
git branch source
 1296  pelican content -o output -s pelicanconf.py
 1297  ghp-import output -b gh-pages
 1298  git push https://github.com/robOcity/robocity.github.com.git gh-pages:master
 1299  ghp-import output -b master
 1300  git checkout master
 1301  git push
## Resources

1. [Documentation: Pelican Stable](https://docs.getpelican.com/en/stable/index.html)
2. [Repository: pelican-ipynb plugin]([pelican-ipynb](https://github.com/danielfrg/pelican-ipynb))
3. [Blog: Matt Makai's Excellent Pelican Posts](https://www.fullstackpython.com/pelican.html)
4. [Blog: Some Tips for Using Jupyter Notebooks with Pelican](https://pmbaumgartner.github.io/blog/jupyter-notebooks-for-pelican/)
5. [Blog: Hacking my way to a Jupyter notebook powered blog](https://nipunbatra.github.io/blog/2017/Jupyter-powered-blog.html)
