# Copyright (c) 2018-present. This file is part of V-Sekai https://v-sekai.org/.
# SaracenOne & K. S. Ernest (Fire) Lee & Lyuma & MMMaellon & Contributors
# generative_sidecar_test.exs
# SPDX-License-Identifier: MIT

defmodule GenerativeSidecarTest do
  use ExUnit.Case
  doctest GenerativeSidecar

  test "greets the world" do
    assert GenerativeSidecar.hello() == :world
  end
end
