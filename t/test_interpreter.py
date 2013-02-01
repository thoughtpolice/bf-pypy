from bf.main import run

def test_interp():
    run('++++++')
    # nothing

def test_A(capfd):
    run("""> +++++
           [ < +++++ +++++ +++ > - ]
           < .
        """)
    out, err = capfd.readouterr()
    assert err == u''
    assert out == 'A'
