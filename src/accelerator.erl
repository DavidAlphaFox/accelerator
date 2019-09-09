%%%-------------------------------------------------------------------
%%% @author bj
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 04. 九月 2019 下午3:06
%%%-------------------------------------------------------------------
-module(accelerator).
-author("bj").

-export([main/0]).


log(Arg) ->
  io:format("~p~n", [Arg]).

%%log(Format, Args) ->
%%  io:format(Format, Args).


relay_loop(L_socket, R_socket) ->
  receive
    {tcp, L_socket, Bin} ->
      log(binary_to_list(Bin)),
      gen_tcp:send(R_socket, Bin),
      relay_loop(L_socket, R_socket);

    {tcp, R_socket, Bin} ->
      gen_tcp:send(L_socket, Bin),
      relay_loop(L_socket, R_socket);

    {tcp_closed, _} ->
      log("closed")
  end.


handle(Socket) ->
%%  inet:setopts(Socket, [{active, true}]),
  {ok, R_socket} = gen_tcp:connect("127.0.0.1", 1082, [binary, {active, true}]),
  relay_loop(Socket, R_socket).


main() ->
  io:format("test~n"),
  tcp_server:start_serv(1083, fun (S) -> handle(S) end).