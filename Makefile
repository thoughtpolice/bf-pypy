ifeq ($(V),1)
Q=
else
Q=@
endif

P?=targetbf
OUT?=bf-c.exe
ifndef P
	$(error Need to define P)
endif

PY?=pypy
PYPYSRC?=$(HOME)/code/pypy
RPYTHONC?=$(PYPYSRC)/rpython/bin/rpython

OPTS=-O$(OPT) --output $(OUT)
OPTS+= $(EXTRA_OPTS)

all:
	$(Q)echo "Run 'make compile OPT=...' or 'make interpret'"
compile:
	$(Q)PYTHONPATH=$(PYPYSRC) $(RPYTHONC) $(OPTS) $(P).py
interpret:
	$(Q)echo "Run this to interpret with regular python and avoid compilation."
	$(Q)echo "Note, this is ridiculously slow, and mostly useful for debugging"
	$(Q)echo "and fast developer turnaround!"
	$(Q)echo
	$(Q)echo 'PYTHONPATH=$(PYPYSRC) $(PY) $(P).py'
test:
	$(Q)PYTHONPATH=$(PYPYSRC) $(PYPYSRC)/pytest.py t
jitviewer:
	$(Q)PYTHONPATH=$(PYPYSRC) jitviewer.py $(JITLOG)
clean:
	$(Q)rm -f *~ *.exe *.pyc *.jitlog
	$(Q)rm -f bf/*~ bf/*.pyc
	$(Q)rm -f test/*~ test/*.pyc
	$(Q)rm -rf __pycache__ bf/__pycache__ test/__pycache__

.PHONY: test
