import re
import subprocess as s

def execute(inp, commands):
    procs = []
    end = inp.encode()

    for i, command in enumerate(commands):
        procs.append(
            s.Popen(command, stdin=s.PIPE, stdout=s.PIPE)
        )

        end, _ = procs[i].communicate(end)

    return end.decode()
