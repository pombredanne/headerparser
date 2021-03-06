import pytest
from   six          import StringIO
from   headerparser import HeaderParser, MissingBodyError

def test_simple():
    parser = HeaderParser()
    parser.add_field('Foo')
    parser.add_field('Bar')
    parser.add_field('Baz')
    fp = StringIO(
        'Foo: red\n'
        'Bar: green\n'
        'Baz: blue\n'
        '\n'
        'This body is not consumed.\n'
    )
    msg = parser.parse_next_stanza(fp)
    assert dict(msg) == {"Foo": "red", "Bar": "green", "Baz": "blue"}
    assert msg.body is None
    assert fp.read() == 'This body is not consumed.\n'

def test_simple_string():
    parser = HeaderParser()
    parser.add_field('Foo')
    parser.add_field('Bar')
    parser.add_field('Baz')
    msg, rest = parser.parse_next_stanza_string(
        'Foo: red\n'
        'Bar: green\n'
        'Baz: blue\n'
        '\n'
        'This body is not consumed.\n'
    )
    assert dict(msg) == {"Foo": "red", "Bar": "green", "Baz": "blue"}
    assert msg.body is None
    assert rest == 'This body is not consumed.\n'

def test_body_true():
    parser = HeaderParser(body=True)
    parser.add_field('Foo')
    parser.add_field('Bar')
    parser.add_field('Baz')
    fp = StringIO(
        'Foo: red\n'
        'Bar: green\n'
        'Baz: blue\n'
        '\n'
        'This body is not consumed.\n'
    )
    with pytest.raises(MissingBodyError):
        parser.parse_next_stanza(fp)

def test_body_true_string():
    parser = HeaderParser(body=True)
    parser.add_field('Foo')
    parser.add_field('Bar')
    parser.add_field('Baz')
    with pytest.raises(MissingBodyError):
        parser.parse_next_stanza_string(
            'Foo: red\n'
            'Bar: green\n'
            'Baz: blue\n'
            '\n'
            'This body is not consumed.\n'
        )
