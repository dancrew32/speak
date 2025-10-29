make:
	vim makefile

venv:
	virtualenv -p python3 venv

back_deps:
	./venv/bin/pip3 install -r requirements.txt

front_deps:
	npm i

deps: back_deps front_deps

run_back:
	./venv/bin/python main.py

run:
	npm start

front_pretty:
	./node_modules/.bin/prettier "*.{js,css}" --ignore-path .gitignore --write

back_pretty:
	./venv/bin/black main.py

pretty: back_pretty front_pretty

checkin: pretty
	git add -Ap && git commit && git push
