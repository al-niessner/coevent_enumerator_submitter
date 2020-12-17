'''helper module to connect between the _context.json file and python code'''

import json

_CTXT = {'coverage_threshold_percent':70,
         'post_count':3,
         'post_buffer_in_seconds':86400,
         'prior_count':3,
         'prior_buffer_in_seconds':86400}
def _context (name:str):
    '''private function'''
    if not _CTXT:
        with open ('_context.json', 'rt') as file: _CTXT.update(json.load(file))
        pass
    return _CTXT[name]

# pylint: disable=missing-function-docstring

@property
def coverage_threshold_percent(): return _context ('coverage_threshold_percent')

@property
def post_count(): return _context ('post_count')

@property
def post_buffer_in_seconds(): return _context ('post_buffer_in_seconds')

@property
def prior_count(): return _context ('prior_count')

@property
def prior_buffer_in_seconds(): return _context ('prior_buffer_in_seconds')

# pylint: enable=missing-function-docstring
