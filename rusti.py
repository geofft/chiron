import json
import requests

import chiron

irc_template = """\
#![allow(dead_code, unused_variables)]
#![allow(unused_features)]

fn show<T: std::fmt::Debug>(e: T) { println!("{:?}", e) }

fn main() {
    show({
        %(input)s
    });
}"""

def evaluate(code):
    code = irc_template % {"input": code}

    payload = json.dumps(dict(code=code, version="beta", optimize="2"))
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'rusti for MIT Zephyr (geofft@ldpreload.com)'}
    response = requests.post('https://play.rust-lang.org/evaluate.json',
                             data=payload, headers=headers)
    j = response.json()
    if 'error' in j:
        out = 'Error: ' + j['error']
    else:
        out = j['result']

    if len(out) > 5000:
        return chiron.Response('rusti', "more than 5000 bytes of output; bailing out")

    out = out.replace(u"\xff", u"", 1)
    out = out.decode(errors="replace")

    return chiron.Response('rusti', out)

