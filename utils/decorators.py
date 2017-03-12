from google.appengine.api import memcache


def validate_csrf(handler):
    def wrapper(self, *args, **kwargs):
        csrf_token = self.request.get("csrf_token")
        mem_token = memcache.get(key=csrf_token)

        # check if token exist in memcache
        if mem_token:
            return handler(self, *args, **kwargs)
        else:
            return self.write("Ha, you are hacker - you shall not pass !")

    return wrapper
