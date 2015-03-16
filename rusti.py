import json
import requests

irc_template = """\
#![feature(asm, simd, thread_local, unsafe_destructor)]
#![feature(core, libc, collections, std_misc, io, path)]
#![allow(dead_code, unused_variables)]
#![allow(unused_features)]

extern crate libc;

fn show<T: std::fmt::Debug>(e: T) { println!("{:?}", e) }

fn main() {
    show({
        %(input)s
    });
}"""

def evaluate(code):
    code = irc_template % {"input": code}

    payload = json.dumps(dict(code=code, version="master", optimize="2"))
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'rusti for MIT Zephyr (geofft@ldpreload.com)'}
    response = requests.post('https://play.rust-lang.org/evaluate.json',
                             data=payload, headers=headers)
    out = response.json()['result']

    if len(out) > 5000:
        return "more than 5000 bytes of output; bailing out"

    out = out.replace(u"\xff", u"", 1)
    out = out.decode(errors="replace")

    return 'rusti', out

