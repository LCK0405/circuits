#!/usr/bin/env python


import pytest

from circuits import Component, Event


class Hello(Event):
    """Hello Event"""

    success = True


class App(Component):

    channel = "app"

    def hello(self):
        return "Hello World!"


@pytest.fixture(scope="module")
def app(request, manager, watcher):
    app = App().register(manager)
    assert watcher.wait("registered")

    def finalizer():
        app.unregister()

    request.addfinalizer(finalizer)

    return app


def test(manager, watcher, app):
    x = manager.fire(Hello(), app)
    assert watcher.wait("hello_success")

    value = x.value
    assert value == "Hello World!"
