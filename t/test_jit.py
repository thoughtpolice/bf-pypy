from rpython.jit.metainterp.test.support import LLJitMixin
from bf.main import run

class TestJit(LLJitMixin):
    def test_jit(self):
        codes = [
            # Print 'A'
            "> +++++ [ < +++++ +++++ +++ > - ] < ."

            # Print alphabet
          , """> ++++ ++++ [ > ++++ ++++ < - ]
               < +++ [ > ++++ ++++ < - ] > ++ [ > +. < - ]
            """
            ]

        def main(i): run(codes[i])
        for i, _ in enumerate(codes):
            self.meta_interp(main, [i], listops=True)
