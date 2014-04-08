from collections import namedtuple


Formatter = namedtuple('Formatter', ['name', 'format'])

uppercased = Formatter('uppercased', lambda s: s.upper())
lowercased = Formatter('lowercased', lambda s: s.lower())
environ = Formatter('environ', lambda s: s.strip().upper().replace(' ', '_'))
