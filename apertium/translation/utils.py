import sys

import apertium
from apertium.utils import to_alpha3_code, execute, start_pipeline, parse_mode_file


ParsedModes = namedtuple('ParsedModes', 'do_flush commands')

def calculate_paths(start):
    nodes = set()
    for pair in map(lambda x: x.split('-'), apertium.pairs):
        nodes.add(pair[0])
        nodes.add(pair[1])
    dists = {}
    prevs = {}
    dists[start] = 0

    while nodes:
        u = min(nodes, key=lambda u: dists.get(u, sys.maxsize))
        nodes.remove(u)
        for v in apertium.pairs_graph.get(u, []):
            if v in nodes:
                other = dists.get(u, sys.maxsize) + 1   # TODO: weight(u, v) -- lower weight = better translation
                if other < dists.get(v, sys.maxsize):
                    dists[v] = other
                    prevs[v] = u

    apertium.paths[start] = {}
    for u in prevs:
        prev = prevs[u]
        path = [u]
        while prev:
            path.append(prev)
            prev = prevs.get(prev)
        apertium.paths[start][u] = list(reversed(path))


def init_paths():
        for lang in apertium.pairs_graph:
            calculate_paths(lang)

def init_pairs_graph():
    for pair in apertium.pairs:
        lang1, lang2 = pair.split('-')
        if lang1 in apertium.pairs_graph:
            apertium.pairs_graph[lang1].append(lang2)
        else:
            apertium.pairs_graph[lang1] = [lang2]

def cmd_needs_z(cmd):
    exceptions = r'^\s*(vislcg3|cg-mwesplit|hfst-tokeni[sz]e|divvun-suggest)'
    return re.match(exceptions, cmd) is None



def get_pipe_cmds(l1, l2):
    if (l1, l2) not in apertium.pipeline_cmds:
        mode_path = apertium.pairs['%s-%s' % (l1, l2)]
        apertium.pipeline_cmds[(l1, l2)] = parse_mode_file(mode_path)
    return apertium.pipeline_cmds[(l1, l2)]

def should_start_pipe(l1, l2):
        pipes = apertium.pipelines.get((l1, l2), [])
        if pipes == []:
            print('%s-%s not in pipelines of this process'
                         l1, l2)
            return True
        else:
            min_p = pipes[0]
            if len(pipes) < apertium.max_pipes_per_pair and min_p.users > apertium.max_users_per_pipe:
                print('%s-%s has ≥%d users per pipe but only %d pipes',
                             l1, l2, min_p.users, len(pipes))
                return True
            else:
                return False

def translate_nul_flush(to_translate, pipeline, unsafe_deformat, unsafe_reformat):
    proc_in, proc_out = pipeline.inpipe, pipeline.outpipe
    deformat, reformat = validate_formatters(unsafe_deformat, unsafe_reformat)

    if deformat:
        proc_deformat = Popen(deformat, stdin=PIPE, stdout=PIPE)
        proc_deformat.stdin.write(bytes(to_translate, 'utf-8'))
        deformatted = proc_deformat.communicate()[0]
        check_ret_code('Deformatter', proc_deformat)
    else:
        deformatted = bytes(to_translate, 'utf-8')

    proc_in.stdin.write(deformatted)
    proc_in.stdin.write(bytes('\0', 'utf-8'))
    # TODO: PipeIOStream has no flush, but seems to work anyway?
    # proc_in.stdin.flush()

    # TODO: If the output has no \0, this hangs, locking the
    # pipeline. If there's no way to put a timeout right here, we
    # might need a timeout using Pipeline.use(), like servlet.py's
    # cleanable but called *before* trying to translate anew
    output = yield gen.Task(proc_out.stdout.read_until, bytes('\0', 'utf-8'))

    if reformat:
        proc_reformat = Popen(reformat, stdin=PIPE, stdout=PIPE)
        proc_reformat.stdin.write(output)
        result = proc_reformat.communicate()[0]
        check_ret_code('Reformatter', proc_reformat)
    else:
        result = re.sub(rb'\0$', b'', output)
    return result.decode('utf-8')



class FlushingPipeline(Pipeline):
    def __init__(self, commands):
        self.inpipe, self.outpipe = start_pipeline(commands)

    def __del__(self):
        print('shutting down FlushingPipeline that was used times')

    def translate(self, to_translate, nosplit=False, deformat=True, reformat=True):
        if nosplit:
            res = translate_nul_flush(to_translate, self, deformat, reformat)
            return res
        else:
            all_split = split_for_translation(to_translate, n_users=self.users)
            parts = [translate_nul_flush(part, self, deformat, reformat)
                           for part in all_split]
            return ''.join(parts)


class SimplePipeline(Pipeline):
    def __init__(self, commands):
        self.commands = list(commands)

    def translate(self, to_translate, nosplit='ignored', deformat='ignored', reformat='ignored'):
            res = execute(to_translate, self.commands)
            return res

def make_pipeline(modes_parsed):
    if modes_parsed.do_flush:
        return FlushingPipeline(modes_parsed.commands)
    else:
        return SimplePipeline(modes_parsed.commands)

def get_pipeline(pair):
        (l1, l2) = pair
        if should_start_pipe(l1, l2):
            print('Starting up a new pipeline for %s-%s …', l1, l2)
            if pair not in apertium.pipelines:
                apertium.pipelines[pair] = []
            p = make_pipeline(get_pipe_cmds(l1, l2))
            heapq.heappush(apertium.pipelines[pair], p)
        return apertium.pipelines[pair][0]