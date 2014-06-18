django-routes
=============

** WORK IN PROGRESS, NON-FUNCTIONAL **

Simple application to manage dynamic routes inside django admin with apphooks
ala django-cms

## Usage

Clone this repository and install the package:
```
git clone https://github.com/fmartingr/django-routes.git
python setup.py install
```

Add routes at the end of your `INSTALLED_APPS`

```
INSTALLED_APPS = (
    # ...
    'routes'
)
```

Add *routes* `include` URLConf to your main `urls.py`:

```
urlpatterns = (
    # At the end:
    url(r'^', include('routes.urls')),
)
```

Hook apps

```
# routes_app.py in your app to hook
from routes.app_base import App
from routes.apphook_pool import apphook_pool


class BlogApp(App):
    name = 'Blog'
    urls = [
        'blog.urls',
    ]

apphook_pool.register(BlogApp)
```

Go to the admin and configure your stuff!

## License

See LICENSE file
