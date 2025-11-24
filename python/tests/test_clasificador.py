from clasificador import clasificar

def test_empty():
    r = clasificar('')
    assert r['label'] == 'empty'

def test_normal():
    r = clasificar('get temp')
    assert r['label'] in ('normal', 'desconocido')

def test_exploit_keyword():
    r = clasificar('sudo passwd root')
    assert r['label'] == 'exploit'
