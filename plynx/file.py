from bson.objectid import ObjectId
from . import  MissingArgumentError, InvalidTypeArgumentError, Inputs, Params, \
    Outputs, BaseNode

REQUIRED_ARGUMENTS = {
    'id',
}

ARGUMENT_TYPES = {
    'id': basestring,
    'title': basestring,
}


class File(BaseNode):
    def __init__(self, **kwargs):
        super(File, self).__init__()
        for key in REQUIRED_ARGUMENTS:
            if key not in kwargs:
                raise MissingArgumentError('`{}` is requered'.format(key))
        for arg_name, arg_type in ARGUMENT_TYPES.items():
            if arg_name in kwargs and not isinstance(kwargs[arg_name], arg_type):
                raise InvalidTypeArgumentError('`{}` is expected to be an instance of {}'.format(key, arg_type))

        self._id = ObjectId()
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')

        self.derived_from = kwargs.get('id', '')
        if not self.derived_from:
            raise MissingArgumentError('`id` is requered')
        self.derived_from = self.derived_from

        self.inputs = Inputs([])
        self.params = Params([])
        self.outputs = Outputs(self, ['out'])

        # same values across all files
        self.node_type = 'file'
        self.block_running_status = 'STATIC'
