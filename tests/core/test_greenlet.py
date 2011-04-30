#!/usr/bin/env python

import pytest

from circuits import Component, Event


class Foo(Event):
    """Foo Event"""


class Bar(Event):
    """Bar Event"""

class Bar2(Event):
    """Bar Event"""


class FooDone(Event):
    """fire when Foo is done"""


class BarDone(Event):
    """fired when Bar is done"""


class Test(Component):

    def test_wait_class(self):
        x = self.fire(Bar())
        self.waitEvent(BarDone, 30)
        return x.value

    def test_wait_instance(self):
        e = BarDone()
        x = self.fire(Bar2(e))
        self.waitEvent(e, 30)
        return x.value

    def bar(self):
        self.fire(BarDone())
        return "Foobar!"

    def bar2(self, e):
        self.fire(e)
        return "Foobar!"


def test_wait_class():
    test = Test()
    test.start()

    x = test.fire(Foo(), "test_wait_class")
    pytest.wait_event(test, "bardone")
    print(repr(x.value))
    value = x.value
    assert value == "Foobar!"

    test.stop()


def test_wait_instance():
    test = Test()
    test.start()

    e = Foo()
    x = test.fire(e, "test_wait_instance")
    pytest.wait_event(test, "bardone")

    value = x.value
    assert value == "Foobar!"

    test.stop()

