%%%-------------------------------------------------------------------
%%% @author bj
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 23. 四月 2019 下午4:52
%%%-------------------------------------------------------------------
-module(tcp_server).
-author("bj").

%% API
-export([start_serv/2]).

start_serv(Port, Handle) ->
  {ok, Listen} = gen_tcp:listen(Port, [
    binary,
    {active, false},
    {reuseaddr, true}]),
  spawn(fun() -> tcp_listen(Listen, Handle) end),
  receive _ -> ok end.

tcp_listen(Listen, Handle) ->
  {ok, Socket} = gen_tcp:accept(Listen),
  spawn(fun() -> tcp_listen(Listen, Handle) end),
  Handle(Socket).