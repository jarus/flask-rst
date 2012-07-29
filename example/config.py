SITE_NAME = "My Blog"
AUTHOR_NAME = "Me"

MODULES = {
    'flaskrst.modules.page': {},
    'flaskrst.modules.blog': {
        'body_as_summary_fallback': True
    },
    'flaskrst.modules.archive': {},
    'flaskrst.modules.tags': {},
    'flaskrst.modules.atom': {},
    'flaskrst.modules.pygments': {
        'style': 'tango'
    },
    'flaskrst.modules.github': {},
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