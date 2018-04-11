import json
import requests

class ApiActionError(RuntimeError):
    pass

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

def _save_graph(graph, action, client):
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
                'action': action
                }
            })
        )
    if not response.ok:
        raise ApiActionError(response.content)
    content = json.loads(response.content)
    if content['status'].upper() != 'SUCCESS':
        raise ApiActionError(content['message'])
    return content['message']
