from bf.jit import run

def test_interp():
    run('++++++', False)
    # nothing

def test_A(capfd):
    run("""> +++++
           [ < +++++ +++++ +++ > - ]
           < .
        """, False)
    out, err = capfd.readouterr()
    assert err == u''
    assert out == 'A'
