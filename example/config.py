SITE_NAME = "My Blog"
AUTHOR_NAME = "Me"

MODULES = {
    'flaskrst.modules.page': {},
    'flaskrst.modules.blog': {
        'body_as_summary_fallback': True
    },
    'flaskrst.modules.archive': {},
    'flaskrst.modules.tags': {
        'activate_atomfeeds_per_tag': True
        },
    'flaskrst.modules.atom': {},
    'flaskrst.modules.pygments': {
        'style': 'tango'
    },
    'flaskrst.modules.github': {},
    'flaskrst.modules.disqus': {
        'active': False,
        'shortname': 'example' # Change this to your disqus shortname
    },
}

NAVIGATION = [
    {
        'route': 'blog.index',
        'label': 'blog'
        },
    {
        'route': 'archive.index',
        'label': 'archive'
        },
    {
        'route': 'page.show',
        'label': 'about',
        'file_path': 'about'
        }
]

STYLESHEETS = [
    '/static/style.css'
]
