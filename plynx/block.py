import copy
from bson.objectid import ObjectId
from . import  InvalidTypeArgumentError, MissingArgumentError,\
    Inputs, Outputs, Params, BaseNode

REQUIRED_ARGUMENTS = {
    'id',
    'title'
}

ARGUMENT_TYPES = {
    'id': basestring,
    'title': basestring,
    'description': basestring,
    'inputs': list,
    'params': list,
    'outputs': list
}


def Block(**kwargs):
    class BlockClass(BaseNode):
        def __init__(self, **extra_args):
            super(BlockClass, self).__init__()
            args = copy.deepcopy(kwargs)
            args.update(extra_args)
            for key in REQUIRED_ARGUMENTS:
                if key not in args:
                    raise MissingArgumentError('`{}` is requered'.format(key))
            for arg_name, arg_type in ARGUMENT_TYPES.items():
                if arg_name in args and not isinstance(args[arg_name], arg_type):
                    raise InvalidTypeArgumentError('`{}` is expected to be an instance of {}'.format(key, arg_type))

            self._id = ObjectId()
            self.title = extra_args.get('title', kwargs.get('title', ''))
            self.description = extra_args.get('title', kwargs.get('description', ''))

            self.derived_from = args.get('id', '')
            if not self.derived_from:
                raise MissingArgumentError('`id` is requered')
            self.derived_from = self.derived_from

            self.inputs = Inputs(args.get('inputs', []), **args)
            self.params = Params(args.get('params', []), **args)
            self.outputs = Outputs(self, args.get('outputs', []))

            # same values across all blocks
            self.node_type = 'block'
            self.block_running_status = ''

    return BlockClass
