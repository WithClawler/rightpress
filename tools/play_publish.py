#!/usr/bin/env python3
"""Upload a signed AAB to a Google Play testing track with the Play Developer API.

Uses only the standard library plus the system `openssl`. The service-account key is
read from GOOGLE_PLAY_SERVICE_ACCOUNT_JSON (default below) and handed to openssl via a
pipe, so it never reaches argv, temp files or logs.

  python3 tools/play_publish.py check
  python3 tools/play_publish.py upload --aab output/release-1.0.1/RightPress-1.0.1-11.aab
  python3 tools/play_publish.py status

Release notes come from fastlane/metadata/android/<lang>/changelogs/<versionCode>.txt.
"""
import argparse, base64, json, os, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

PACKAGE = 'io.github.doctor_clawler.rightpress'
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KEY = Path.home() / '.config/works/google-play/play-publisher.json'
API = f'https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{PACKAGE}'
UPLOAD = f'https://androidpublisher.googleapis.com/upload/androidpublisher/v3/applications/{PACKAGE}'


def b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=')


def access_token():
    key = json.loads(Path(os.environ.get('GOOGLE_PLAY_SERVICE_ACCOUNT_JSON', DEFAULT_KEY)).read_text())
    now = int(time.time())
    claims = {'iss': key['client_email'], 'scope': 'https://www.googleapis.com/auth/androidpublisher',
              'aud': key['token_uri'], 'iat': now, 'exp': now + 3600}
    unsigned = b64(json.dumps({'alg': 'RS256', 'typ': 'JWT'}).encode()) + b'.' + b64(json.dumps(claims).encode())
    read_end, write_end = os.pipe()
    os.write(write_end, key['private_key'].encode())
    os.close(write_end)
    try:
        signature = subprocess.run(['openssl', 'dgst', '-sha256', '-sign', f'/dev/fd/{read_end}'], input=unsigned,
                                   pass_fds=(read_end,), capture_output=True, check=True).stdout
    finally:
        os.close(read_end)
    body = urllib.parse.urlencode({'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                                   'assertion': (unsigned + b'.' + b64(signature)).decode()}).encode()
    with urllib.request.urlopen(urllib.request.Request(key['token_uri'], data=body), timeout=60) as response:
        return key['client_email'], json.load(response)['access_token']


class Play:
    def __init__(self):
        self.account, self.token = access_token()

    def call(self, method, url, body=None, data=None, content_type='application/json'):
        if body is not None:
            data = json.dumps(body).encode()
        request = urllib.request.Request(url, data=data, method=method,
                                         headers={'Authorization': f'Bearer {self.token}', 'Content-Type': content_type})
        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                raw = response.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors='replace')
            try:
                detail = json.loads(detail)['error']['message']
            except (ValueError, KeyError):
                pass
            raise SystemExit(f'{method} {url.split(PACKAGE)[-1] or "/"} failed: HTTP {error.code}: {detail}')

    def edit(self):
        return self.call('POST', f'{API}/edits', {})['id']

    def discard(self, edit):
        self.call('DELETE', f'{API}/edits/{edit}')

    def tracks(self, edit):
        return self.call('GET', f'{API}/edits/{edit}/tracks').get('tracks', [])


def release_notes(version_code):
    notes = []
    for path in sorted((ROOT / 'fastlane/metadata/android').glob(f'*/changelogs/{version_code}.txt')):
        text = path.read_text().strip()
        if len(text) > 500:
            raise SystemExit(f'{path} exceeds Play\'s 500-character release-note limit')
        notes.append({'language': path.parts[-3], 'text': text})
    return notes


def summarize(tracks):
    return [{'track': t['track'], 'releases': [{k: r.get(k) for k in ('name', 'versionCodes', 'status')}
                                                for r in t.get('releases', [])]} for t in tracks]


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('check', help='verify API access without changing anything')
    sub.add_parser('status', help='read every track')
    upload = sub.add_parser('upload')
    upload.add_argument('--aab', required=True, type=Path)
    upload.add_argument('--track', default='internal', choices=['internal', 'alpha', 'beta'])
    upload.add_argument('--name', help='release name shown in Play Console (defaults to versionName)')
    args = parser.parse_args()

    play = Play()
    if args.command in ('check', 'status'):
        edit = play.edit()
        try:
            print(json.dumps({'account': play.account, 'package': PACKAGE, 'tracks': summarize(play.tracks(edit))},
                             indent=2, ensure_ascii=False))
        finally:
            play.discard(edit)
        return

    edit = play.edit()
    committed = False
    try:
        bundle = play.call('POST', f'{UPLOAD}/edits/{edit}/bundles?uploadType=media',
                           data=args.aab.read_bytes(), content_type='application/octet-stream')
        code = bundle['versionCode']
        notes = release_notes(code)
        release = {'versionCodes': [str(code)], 'status': 'completed', 'releaseNotes': notes}
        if args.name:
            release['name'] = args.name
        play.call('PUT', f'{API}/edits/{edit}/tracks/{args.track}', {'track': args.track, 'releases': [release]})
        play.call('POST', f'{API}/edits/{edit}:commit')
        committed = True
        print(json.dumps({'uploaded': {'versionCode': code, 'sha256': bundle.get('sha256')}, 'track': args.track,
                          'releaseNotes': [n['language'] for n in notes]}, indent=2))
    finally:
        if not committed:
            play.discard(edit)
    readback = play.edit()
    try:
        print(json.dumps({'readback': summarize(play.tracks(readback))}, indent=2, ensure_ascii=False))
    finally:
        play.discard(readback)


if __name__ == '__main__':
    sys.exit(main())
