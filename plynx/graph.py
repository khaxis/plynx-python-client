from . import InvalidTypeArgumentError, BaseNode, File, Block
from . import _get_obj, _save_graph
from collections import deque
import json
import requests
import copy
import collections

def update_recursive(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update_recursive(d.get(k, {}), v)
        elif isinstance(v, list):
            for v_item in v:
                if 'name' in v_item:
                    for d_item in d[k]:
                        if 'name' in d_item and d_item['name'] == v_item['name']:
                            update_recursive(d_item, v_item)
                else:
                    d[k].append(v_item)
        else:
            d[k] = v if v else d[k]
    return d

def traverse_nodes(graph, targets):
    nodes = []
    visited_nodes = set()
    to_visit = deque(targets)
    while len(to_visit) > 0:
        node = to_visit.popleft()
        if node._id in visited_nodes:
            continue
        visited_nodes.add(node._id)
        nodes.append(node)
        for name, output_items in node.inputs.items():
            for output_item in output_items:
                if output_item.node._id in visited_nodes:
                    continue
                to_visit.append(output_item.node)
    return nodes

class Graph(object):
    def __init__(self, client=None, title=None, description=None, targets=None):
        self.client = client
        self.title = title or ''
        self.description = description or ''
        self.targets = targets
        if not isinstance(targets, list):
            self.targets = [targets]
        for target in self.targets:
            if not isinstance(target, BaseNode):
                raise InvalidTypeArgumentError('Target is expected to be an instance of {}, found `{}`'.format(BaseNode, type(target)))

    def _dictify(self):
        nodes = [node for node in traverse_nodes(self, self.targets)]
        plynx_nodes = {}
        for node_type, derived_from in set([(n.node_type, n.derived_from) for n in nodes]):
            obj = _get_obj('{}s'.format(node_type), derived_from, self.client)
            plynx_nodes[derived_from] = obj

        blocks = []
        for node in nodes:
            node_dict = node._dictify()
            plynx_node = copy.deepcopy(plynx_nodes[node.derived_from])
            update_recursive(plynx_node, node_dict)
            blocks.append(plynx_node)

        graph = {
            'title': self.title,
            'description': self.description,
            'graph_running_status': 'CREATED',
            'blocks': blocks
        }
        return graph

    def save(self):
        d = self._dictify()
        _save_graph(graph=d, action='SAVE', client=self.client)
        return self

    def approve(self):
        d = self._dictify()
        _save_graph(graph=d, action='APPROVE', client=self.client)
        return self

    def run(self):
        return self
