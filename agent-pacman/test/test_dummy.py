# This is a test file take from the PyCharm website
# http://www.jetbrains.com/pycharm/quickstart/#BeforeStart
from unittest import TestCase

__author__ = 'aortegag'


class Conference(object):
    def __init__(self):
        self.talks = []

    def get_talk_at(self, time):
        for start, end, name in self.talks:
            if time >= start and time < end:
                return name

    def add_talk(self, start, end, name):
        self.talks.append((start,end,name))


class ConferenceTest(TestCase):
    def setUp(self):
        self.conference = Conference()

    def empty_test(self):
        self.assertEqual(None, self.conference.get_talk_at(10))

    def test_talk(self):
        demo = "PyCharm Demo"
        self.conference.add_talk(10, 12, "%s" % demo)
        self.assertEqual(demo, self.conference.get_talk_at(11))