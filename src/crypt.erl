%%%-------------------------------------------------------------------
%%% @author bj
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 09. 九月 2019 下午5:08
%%%-------------------------------------------------------------------
-module(crypt).
-author("bj").

%% API
-export([]).


encrypt(Key, Content) ->
  crypto:block_encrypt()