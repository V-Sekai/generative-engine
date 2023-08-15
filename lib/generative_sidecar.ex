# Copyright (c) 2018-present. This file is part of V-Sekai https://v-sekai.org/.
# SaracenOne & K. S. Ernest (Fire) Lee & Lyuma & MMMaellon & Contributors
# generative_sidecar.ex
# SPDX-License-Identifier: MIT

defmodule GenerativeSidecar do
  use Application

  def start(_type, _args) do
    children = [
      {Task.Supervisor, name: GenerativeSidecar.TaskSupervisor}
    ]

    opts = [strategy: :one_for_one, name: GenerativeSidecar.Supervisor]
    supervisor_pid = Supervisor.start_link(children, opts)

    Process.flag(:trap_exit, true)
    {:ok, blender_pid} = launch_blender()

    Process.monitor(blender_pid)

    supervisor_pid
  end

  def handle_info({:DOWN, _ref, :process, _pid, _reason}, state) do
    IO.puts("Blender process has been stopped")
    {:noreply, state}
  end

  def launch_blender do
    task_fn = fn ->
      {result, _} = System.cmd("blender", ["-P", "generative_engine.py"])
      IO.puts(result)
    end

    Task.Supervisor.start_child(GenerativeSidecar.TaskSupervisor, task_fn)
  end

  def terminate(_reason, _state) do
    IO.puts("Stopping Blender process...")
    System.cmd("pkill", ["-f", "blender"])
    :ok
  end
end
