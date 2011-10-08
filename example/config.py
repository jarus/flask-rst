SITE_NAME = "My Blog"
AUTHOR_NAME = "Me"

MODULES = {
    'page': {
        'active': True
        },
    'blog': {
        'active': True
        },
    'archive': {
        'active': True
        },
    'tags': {
        'active': True
        },
    'pygments': {
        'active': True,
        'style': 'tango'
        }
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
