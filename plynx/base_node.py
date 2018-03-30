import abc, six

class MissingArgumentError(ValueError):
    pass

class InvalidTypeArgumentError(TypeError):
    pass

class NodeAttributeError(AttributeError):
    pass

class NodeProps(object):
    def __init__(self, names):
        super(NodeProps, self).__init__()
        self._pyname_to_name = {
            name.replace('-', '_').replace('.', '_'): name for name in names
        }
        self._name_to_pyname = {v: k for k, v in self._pyname_to_name.items()}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(
                ['{}: {}'.format(
                    pyname, self.__getattribute__(pyname))
                    for pyname in self._pyname_to_name.keys()
                ]
            )
        )

    def __setattr__(self, key, value):
        if '_initialized' in self.__dict__ and self._initialized and key not in self.__dict__:
            raise NodeAttributeError(
                '{} object has no attribute `{}`'
                .format(self.__class__.__name__, key)
            )
        self.__dict__[key] = value

    def __getitem__(self, name):
        return self.__getattribute__(self._name_to_pyname[name])

    def __setitem__(self, name, value):
        return self.__setattr__(self._name_to_pyname[name], value)

    def __iter__(self):
        for name in self._name_to_pyname.keys():
            yield name

    def items(self):
        for name, pyname in self._name_to_pyname.items():
            yield name, self[name]


class Inputs(NodeProps):
    def __init__(self, names, **extra_args):
        super(Inputs, self).__init__(names)
        for pyname in self._pyname_to_name.keys():
            self.__setattr__(pyname, None)
        self._initialized = True
        for name, value in extra_args.items():
            if name in self._pyname_to_name:
                self.__setattr__(pyname, value)

    def __setattr__(self, key, value):
        if '_initialized' in self.__dict__ and self._initialized:
            if isinstance(value, list):
                for item in value:
                    if not isinstance(item, OutputItem):
                        raise InvalidTypeArgumentError('Expected type `{}`, got `{}`'
                            .format(OutputItem, type(item)))
            else:
                if value is not None and not isinstance(value, OutputItem):
                    raise InvalidTypeArgumentError('Expected type `{}`, got `{}`'
                        .format(OutputItem, type(value)))
                value = [value]
        super(Inputs, self).__setattr__(key, value)

    def _dictify(self):
        return [
            {
                'name': pyname,
                'values': [output_item._dictify() for output_item in  self.__getattribute__(pyname)]
            }
            for pyname in self._pyname_to_name.keys()
        ]


class OutputItem(object):
    def __init__(self, node, output_name):
        self.node = node
        self.output_name = output_name

    def __repr__(self):
        return 'OutputItem({}: {})'.format(str(self.node), str(self.output_name))

    def _dictify(self):
        return {
            'output_id': self.output_name,
            'block_id': str(self.node._id),
            'resource_id': None
            }


class Outputs(NodeProps):
    def __init__(self, node, names):
        super(Outputs, self).__init__(names)
        for pyname, name in self._pyname_to_name.items():
            self.__setattr__(pyname, OutputItem(node, name))
        self._initialized = True

    def _dictify(self):
        return []


class Params(NodeProps):
    def __init__(self, names, **extra_args):
        super(Params, self).__init__(names)
        for pyname in self._pyname_to_name.keys():
            self.__setattr__(pyname, None)
        for name, value in extra_args.items():
            if name in self._pyname_to_name:
                self.__setattr__(pyname, value)
        self._initialized = True

    def _dictify(self):
        return [
            {'name': pyname, 'value': self.__getattribute__(pyname)}
            for pyname in self._pyname_to_name.keys()
        ]


@six.add_metaclass(abc.ABCMeta)
class BaseNode():
    def _dictify(self):
        node_dict = {
            '_type': self.node_type,
            'description': self.description,
            'title': self.title,
            'block_running_status': self.block_running_status,
            'inputs': self.inputs._dictify(),
            'parameters': self.params._dictify(),
            'outputs': self.outputs._dictify(),
            'y':0,
            'x':0,
            '_id': str(self._id)

        }
        return node_dict

    def _expand(self, client):
        client
