defmodule GenerativeSidecar do
  use Application

  def start(_type, _args) do
    children = [
      {Task.Supervisor, name: GenerativeSidecar.TaskSupervisor}
    ]

    opts = [strategy: :one_for_one, name: GenerativeSidecar.Supervisor]
    supervisor_pid = Supervisor.start_link(children, opts)

    launch_blender()

    supervisor_pid
  end

  def launch_blender do
    task_fn = fn ->
      {result, _} = System.cmd("blender", ["-P", "generative_engine.py"])
      IO.puts(result)
    end

    Task.Supervisor.start_child(GenerativeSidecar.TaskSupervisor, task_fn)
    :ok
  end
end
