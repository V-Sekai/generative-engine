defmodule GenerativeSidecarTest do
  use ExUnit.Case
  doctest GenerativeSidecar

  test "greets the world" do
    assert GenerativeSidecar.hello() == :world
  end
end
