SITE_NAME = "My Blog"
AUTHOR_NAME = "Me"

MODULES = {
    'page': {
        },
    'blog': {
        },
    'archive': {
        },
    'tags': {
        },
    'pygments': {
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
