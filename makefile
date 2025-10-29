make:
	vim makefile

venv:
	virtualenv -p python3 venv

deps:
	./venv/bin/pip3 install -r requirements.txt

run:
	./venv/bin/python main.py
