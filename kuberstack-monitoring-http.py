import time

import requests
import yaml
from alerts.slack import send_alert as slack_send_alert
from settings import UPDATE_INTERVAL, CONF_PATH


def valid_conf(conf):
    for key in ['defaults', 'domains']:
        if not conf.get(key):
            raise BaseException('Base section "{key}" config section is not defined'.format(key=key))

    for key in ['path', 'status', 'timeout', 'https_valid_check', 'max_timeout']:
        if not conf['defaults'].get(key):
            raise BaseException('Defaults section "{key}" config is not defined'.format(key=key))

    for domain in conf['domains']:
        if not domain.get('host'):
            raise BaseException('"host" parameter in domain section is required')
        for key in domain.keys():
            if key not in ['host', 'port', 'path', 'is_https', 'status', 'timeout', 'https_valid_check']:
                raise BaseException(
                    'Domain section "{key}" is domain {domain} is not valid'.format(key=key, domain=domain['host']))


def load_conf():
    conf = yaml.load(open(CONF_PATH, 'r'))
    valid_conf(conf)
    return conf


def get_url(host, port, path, is_https):
    if is_https:
        schema = 'https'
    else:
        schema = 'http'

    return '{schema}://{host}:{port}{path}'.format(schema=schema, host=host, port=port, path=path)


def get_default_port(is_https):
    if is_https:
        return 443
    else:
        return 80


def check_url(url, timeout, status, https_valid_check, max_timeout):
    result = {'result': True, 'response_time': 0, 'code': 0, 'description': 'None', 'event_type': 'Normal'}

    # Unaccepted error
    try:
        r = requests.get(url, timeout=max_timeout, verify=https_valid_check, allow_redirects=False)
        result['code'] = r.status_code
        result['response_time'] = r.elapsed.total_seconds()
    except Exception as p:
        result['result'] = False
        result['event_type'] = 'Error'
        result['description'] = p
        return result

    # Response time
    if r.elapsed.total_seconds() > timeout:
        result['result'] = False
        result['event_type'] = 'Warning'
        result['description'] = 'Response time > {timeout}: {response_time}'.format(timeout=timeout,
                                                                                    response_time=result['response_time'])
        return result

    # Response status
    if r.status_code != status:
        result['result'] = False
        result['event_type'] = 'Error'
        result['description'] = 'Invalid status code: {code}'.format(code=result['code'])
        return result

    return {'result': True}


def main():
    conf = load_conf()
    max_timeout = conf['defaults']['max_timeout']

    try:
        while not time.sleep(UPDATE_INTERVAL):
            for domain in conf['domains']:
                host = domain.get('host')
                is_https = domain.get('is_https', conf['defaults']['is_https'])
                port = domain.get('port', get_default_port(is_https))
                path = domain.get('path', conf['defaults']['path'])
                status = domain.get('status', conf['defaults']['status'])
                timeout = domain.get('timeout', conf['defaults']['timeout'])
                https_valid_check = domain.get('https_valid_check', conf['defaults']['https_valid_check'])

                url = get_url(host, port, path, is_https)

                res = check_url(url, timeout, status, https_valid_check, max_timeout)
                if res['result']:
                    continue

                slack_send_alert(res['event_type'], url, res['description'], res['code'], res['response_time'])

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
