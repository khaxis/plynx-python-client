from . import ApiActionError
import json
import requests
import logging

def _get_obj(obj_path, obj_id, client):
    response = requests.get(
        '{endpoint}/{path}/{id}'.format(
            endpoint=client.endpoint,
            path=obj_path,
            id=obj_id
            ),
        headers={"Content-Type": "application/json"},
        auth=(client.token, '')
        )
    if not response.ok:
        raise ApiActionError(response.content)
    content = json.loads(response.content)
    return content['data']

def _save_graph(graph, actions, client):
    response = requests.post(
        '{endpoint}/{path}'.format(
            endpoint=client.endpoint,
            path='graphs'
            ),
        headers={"Content-Type": "application/json"},
        auth=(client.token, ''),
        data=json.dumps({
            'body': {
                'graph': graph,
                'actions': actions
                }
            })
        )
    if not response.ok:
        raise ApiActionError(response.content)
    content = json.loads(response.content)
    if content['status'].upper() != 'SUCCESS':
        if content['status'].upper() == 'VALIDATION_FAILED':
            logging.error('Validation error:')
            print_validation_error(content['validation_error'])
        raise ApiActionError(content['message'])
    return content['graph'], content['url']

def print_validation_error(validation_error):
    for child in validation_error['children']:
        validation_code = child['validation_code']
        if validation_code == 'IN_DEPENDENTS':
            print_validation_error(child)
        elif validation_code == 'MISSING_INPUT':
            logging.error('Missing input: `{}`'.format(child['object_id']))
        elif validation_code == 'MISSING_PARAMETER':
            logging.error('Missing parameter: `{}`'.format(child['object_id']))
        else:
            logging.error('Unexpected Error')
