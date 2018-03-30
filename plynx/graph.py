from . import InvalidTypeArgumentError, BaseNode, File, Block
from collections import deque
import json
import requests

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
        blocks = []
        graph = {
            'title': self.title,
            'description': self.description,
            'graph_running_status': 'CREATED',
            'blocks': [node._dictify() for node in traverse_nodes(self, self.targets)]
        }
        return graph

    def save(self):
        print(self._dictify())
        return self
        print('-' * 20)
        response = requests.post(
            self.client.endpoint + '/graphs',
            headers={"Content-Type": "application/json"},
            auth=(self.client.token, ''),
            data=json.dumps({
                'body': {
                    'graph': self._dictify(),
                    'action': 'fake'
                    }
                })
            )
        print json.loads(response.content)
        print('-' * 20)
        return self

    def approve(self):
        """print('-' * 20)
        response = requests.get(
            self.client.endpoint + '/graphs',
            headers={"Content-Type": "application/json"},
            auth=(self.client.token, '')
            )
        print type(response.content)
        print('-' * 20)"""
        return self

    def run(self):
        return self
