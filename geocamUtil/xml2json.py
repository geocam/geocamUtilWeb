#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

"""
xml2json: An XML parsing library that allows you to treat compatible XML
dialects much like JSON.

If you run the library as a script it will read the specified XML file
and output the corresponding JSON format.

Example:

$ cat test.xml
<foo name="hi">
  <baz>A</baz>
  <baz>B</baz>
  <bar id="blah">
    <x>1</x>
    <y>2</y>
  </bar>
</foo>
$ xml2json.py test.xml
{
    "foo": {
        "_name": "hi",
        "bar": {
            "_id": "blah",
            "x": {
                "text": "1"
            },
            "y": {
                "text": "2"
            }
        },
        "baz": [
            {
                "text": "A"
            },
            {
                "text": "B"
            }
        ]
    }
}

You can also use xml2json to parse XML and access its fields like a
Python object.

Example:

>>> from xml2json import xml2struct
>>> obj = xml2struct('test.xml')
>>> print obj.foo.baz[0].text
A

Notes:

Within a tag, subtags are converted to object fields (and, like a Python
dict, the order of the fields is not preserved).  If the same subtag is
specified multiple times, the value of the field becomes a list
containing all of the specified instances in order.

Each attribute on the tag is converted to an object field, with an
underscore prepended on the name to distinguish it from a subtag.

Text within a tag is captured in the special "text" field of the object.
Specifically, to calculate the value of the text field, the converter
concatenates all of the CDATA elements directly contained within the
tag, after stripping leading and trailing whitespace around each
element.

"""

import logging
from xml.parsers import expat

from geocamUtil import anyjson as json
from geocamUtil.dotDict import convertToDotDictRecurse


class ToJsonParser(object):
    def __init__(self):
        self.parser = expat.ParserCreate()
        self.parser.StartElementHandler = self.startElement
        self.parser.EndElementHandler = self.endElement
        self.parser.CharacterDataHandler = self.charData
        self.tagStack = [{}]

    def startElement(self, name, attrs):
        logging.debug('expat startElement %s %s', name, attrs)
        newTag = dict([('_' + k, v)
                       for k, v in attrs.iteritems()])
        top = self.tagStack[-1]
        if name in top:
            if not isinstance(top[name], list):
                top[name] = [top[name]]
            top[name].append(newTag)
        else:
            top[name] = newTag
        self.tagStack.append(newTag)

    def endElement(self, name):
        logging.debug('expat endElement %s', name)
        self.tagStack.pop()

    def charData(self, data):
        logging.debug('charData [%s]', data)
        stripped = data.strip()
        if stripped:
            top = self.tagStack[-1]
            if 'text' not in top:
                top['text'] = ''
            top['text'] += stripped

    def parseString(self, xml):
        self.parser.Parse(xml)
        return self.tagStack[0]

    def parseFile(self, f):
        self.parser.ParseFile(f)
        return self.tagStack[0]


def xml2dict(inName, inputIsString=False):
    if inputIsString:
        return ToJsonParser().parseString(inName)
    else:
        inFile = file(inName, 'r')
        return ToJsonParser().parseFile(inFile)


def xml2struct(inName, inputIsString=False):
    return convertToDotDictRecurse(xml2dict(inName, inputIsString))


def xml2json(inName, outName):
    struct = xml2dict(inName)
    outText = json.dumps(struct, indent=4, sort_keys=True)
    if outName == '-':
        print outText
    else:
        file(outName, 'w').write(outText)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <in.xml> [out.json]')
    parser.add_option('-o', '--output',
                      help='Explicitly specify output file')
    opts, args = parser.parse_args()
    if len(args) == 1:
        (inName,) = args
        outName = '-'
    elif len(args) == 2:
        (inName, outName) = args
    else:
        parser.error('expected 1 or 2 args')
    if opts.output:
        outName = opts.output
    xml2json(inName, outName)


if __name__ == '__main__':
    main()
