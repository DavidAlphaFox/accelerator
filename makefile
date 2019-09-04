main:
	rebar3 compile

dev:
	rebar3 compile
	erl -pa ./_build/default/lib/accelerator/ebin/ -noshell -s accelerator main -s init stop
