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


-record(request, {
  socket,
  adr_type,
  raw_bin,
  host,
  ip,
  port
}).


log(Arg) ->
  io:format("~p~n", [Arg]).

%%log(Format, Args) ->
%%  io:format(Format, Args).


relay_loop(L_socket, R_socket) ->
  receive
    {tcp, L_socket, Bin} ->
      gen_tcp:send(R_socket, Bin),
      relay_loop(L_socket, R_socket);

    {tcp, R_socket, Bin} ->
      gen_tcp:send(L_socket, Bin),
      relay_loop(L_socket, R_socket);

    {tcp_closed, _} ->
      log("closed")
  end.


connect(1, Dst_adr) ->
  <<A:8, B:8, C:8, D:8, Port:16>> = Dst_adr,
  IP = {A, B, C, D},
  log(IP),
  gen_tcp:connect(IP, Port, [binary, {active, true}]);

connect(3, Dst_adr) ->
  <<D_len:8, Host_bytes:D_len/bytes, Port:16>> = Dst_adr,
  Host = binary_to_list(Host_bytes),
  log(Host),
  gen_tcp:connect(Host, Port, [binary, {active, true}]).


handle(Socket) ->
  {ok, <<Ver, Len, _Methods:Len/bytes>>} = gen_tcp:recv(Socket, 0),
  gen_tcp:send(Socket, <<5, 0>>),

  {ok, <<Ver, 1, 0, Adr_type>>} = gen_tcp:recv(Socket, 4),
  {ok, Dst_adr} = gen_tcp:recv(Socket, 0),
  {ok, R_socket} = connect(Adr_type, Dst_adr),
  gen_tcp:send(Socket, <<5, 0, 0, 1, 0, 0, 0, 0, 0, 0>>),
  inet:setopts(Socket, [{active, true}]),
  relay_loop(Socket, R_socket).


main() ->
  io:format("test~n"),
  tcp_server:start_serv(1082, fun (S) -> handle(S) end).