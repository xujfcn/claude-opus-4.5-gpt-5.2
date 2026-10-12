"""Python 3.10+. Offline by default. No credentials or response bodies in reports."""
import argparse
import datetime as dt
import json
import os
import platform
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

HOSTS = {'crazyrouter.com', 'cn.crazyrouter.com', 'api.crazyrouter.com'}
PROTOCOLS = {
    'chat': ('/v1', '/chat/completions', 'gpt-4o-mini'),
    'responses': ('/v1', '/responses', 'gpt-5.6-sol'),
    'messages': ('', '/v1/messages', 'claude-sonnet-4-6'),
    'gemini': ('', '/v1beta/models/{model}:generateContent', 'gemini-3.1-pro'),
}

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def validate_base(base, protocol):
    try:
        u = urlsplit(base)
        if u.scheme != 'https' or u.hostname not in HOSTS or u.username or u.password or u.port not in (None, 443):
            return ['Use an HTTPS Crazyrouter host without credentials or a custom port.']
        if u.query or u.fragment:
            return ['Remove query parameters (including UTM) and fragments from the API base.']
        if u.path.rstrip('/') != PROTOCOLS[protocol][0]:
            return ['This protocol requires a root URL.' if protocol in ('messages', 'gemini') else 'This protocol requires exactly one /v1 suffix.']
        return []
    except ValueError:
        return ['Invalid API base URL.']

def request(url, key, body=None, protocol='chat'):
    headers = {'Content-Type': 'application/json'}
    if protocol == 'gemini': headers['x-goog-api-key'] = key
    elif protocol == 'messages': headers.update({'x-api-key': key, 'anthropic-version': '2023-06-01'})
    else: headers['Authorization'] = 'Bearer ' + key
    req = Request(url, data=json.dumps(body).encode() if body is not None else None, headers=headers)
    try:
        with build_opener(NoRedirect()).open(req, timeout=90) as response:
            raw = response.read(4_000_001)
            if len(raw) > 4_000_000: return response.status, None
            return response.status, json.loads(raw)
    except HTTPError as e:
        return e.code, None
    except (URLError, TimeoutError, OSError, ValueError):
        return None, None

def body_for(protocol, model):
    msg = [{'role': 'user', 'content': 'Reply with OK.'}]
    if protocol == 'responses': return {'model': model, 'input': 'Reply with OK.', 'max_output_tokens': 128}
    if protocol == 'messages': return {'model': model, 'messages': msg, 'max_tokens': 32}
    if protocol == 'gemini': return {'contents': [{'parts': [{'text': 'Reply with OK.'}]}], 'generationConfig': {'maxOutputTokens': 128}}
    return {'model': model, 'messages': msg, 'max_tokens': 32}

def has_output(protocol, data):
    if not isinstance(data, dict): return False
    if protocol == 'chat': return any(x.get('message', {}).get('content') for x in data.get('choices', []))
    if protocol == 'messages': return any(x.get('type') == 'text' and x.get('text') for x in data.get('content', []))
    if protocol == 'responses': return any(c.get('type') == 'output_text' and c.get('text') for x in data.get('output', []) for c in x.get('content', []))
    return any(p.get('text') for x in data.get('candidates', []) for p in x.get('content', {}).get('parts', []))

def diagnose(protocol, base, model, key=None, online=False, inference=False, transport=request):
    errors = validate_base(base, protocol)
    if not model or not all(c.isalnum() or c in '-._/' for c in model): errors.append('Use an exact model ID without whitespace or query parameters.')
    report = {'checked_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'python': platform.python_version(),
              'platform': platform.system(), 'protocol': protocol, 'configuration_valid': not errors,
              'key_present': bool(key), 'errors': errors, 'checks': [],
              'scope': 'A minimal request is not a tool-calling, streaming or full-client compatibility test.'}
    # Never echo invalid URLs/model arguments, which could contain secrets.
    if errors: return report
    report.update(base_url=base.rstrip('/'), model=model)
    if not (online or inference): return report
    if not key: report['errors'].append('Set CRAZYROUTER_API_KEY locally before network checks.'); return report
    origin = 'https://' + urlsplit(base).netloc
    status, data = transport(origin + '/v1/models', key)
    valid = status == 200 and isinstance(data, dict) and isinstance(data.get('data'), list)
    visible = any(x.get('id') == model for x in data['data']) if valid else None
    report['checks'].append({'name': 'discovery', 'status': status, 'valid_response': valid, 'model_listed': visible})
    if not valid:
        report['errors'].append('Discovery failed; check network, credentials and permissions.'); return report
    if inference:
        endpoint = base.rstrip('/') + PROTOCOLS[protocol][1].format(model=quote(model, safe=''))
        status, data = transport(endpoint, key, body_for(protocol, model), protocol)
        output = has_output(protocol, data)
        report['checks'].append({'name': 'inference', 'status': status, 'has_output': output})
        if status != 200 or not output: report['errors'].append('Inference did not produce text; consult the troubleshooting guide for the status and model parameters.')
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--protocol', choices=PROTOCOLS, default='chat')
    parser.add_argument('--base-url'); parser.add_argument('--model')
    parser.add_argument('--online', action='store_true', help='Check authenticated model discovery, without inference.')
    parser.add_argument('--inference', action='store_true', help='Also send one potentially billable minimal text request. No retries.')
    args = parser.parse_args()
    base = args.base_url or ('https://api.crazyrouter.com' if args.protocol == 'gemini' else 'https://crazyrouter.com' + PROTOCOLS[args.protocol][0])
    result = diagnose(args.protocol, base, args.model or PROTOCOLS[args.protocol][2], os.environ.get('CRAZYROUTER_API_KEY'), args.online, args.inference)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return int(bool(result['errors']))

if __name__ == '__main__': raise SystemExit(main())
