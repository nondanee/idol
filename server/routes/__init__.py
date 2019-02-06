from . import feed, active, follow, subscription, like, history, overview, diary, related, search, free

def setup_routes(app):
    app.router.add_route('GET', '/active', active.route)

    app.router.add_route('GET', '/feed/all', feed.all)
    app.router.add_route('GET', '/feed/follow', feed.follow)
    app.router.add_route('GET', '/feed/favor', feed.favor)
    app.router.add_route('GET', '/feed/member/{mid:\d{4}}', feed.member)

    app.router.add_route('GET', '/overview', overview.route)

    app.router.add_route('GET', '/diary/{fid:\d{7}}', diary.route)
    app.router.add_route('GET', '/blog/{fid:\d{7}}', diary.legacy)

    app.router.add_route('GET', '/related/{fid:\d{7}}', related.route)

    app.router.add_route('GET', '/history', history.route)

    app.router.add_route('POST', '/like/create', like.create)
    app.router.add_route('POST', '/like/destroy', like.destroy)

    app.router.add_route('GET', '/follow/manifest', follow.manifest)
    app.router.add_route('POST', '/follow/add', follow.add)
    app.router.add_route('POST', '/follow/remove', follow.remove)

    app.router.add_route('POST', '/subscription/prepare', subscription.prepare)
    app.router.add_route('POST', '/subscription/confirm', subscription.confirm)
    app.router.add_route('POST', '/subscription/cancel', subscription.cancel)

#     app.router.add_route('GET', '/search', search.route)
    app.router.add_route('GET', '/free', free.route)