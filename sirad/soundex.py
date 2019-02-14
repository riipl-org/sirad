"""
soundex function from jellyfish package (https://github.com/jamesturk/jellyfish)

Copyright (c) 2015, James Turk
Copyright (c) 2015, Sunlight Foundation

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import unicodedata


def _normalize(s):
    return unicodedata.normalize('NFKD', s)


def _check_type(s):
    if not isinstance(s, str):
        raise TypeError('expected str or unicode, got %s' % type(s).__name__)


def soundex(s):

    _check_type(s)

    if not s:
        return ''

    s = _normalize(s)
    s = s.upper()

    replacements = (('BFPV', '1'),
                    ('CGJKQSXZ', '2'),
                    ('DT', '3'),
                    ('L', '4'),
                    ('MN', '5'),
                    ('R', '6'))
    result = [s[0]]
    count = 1

    # find would-be replacment for first character
    for lset, sub in replacements:
        if s[0] in lset:
            last = sub
            break
    else:
        last = None

    for letter in s[1:]:
        for lset, sub in replacements:
            if letter in lset:
                if sub != last:
                    result.append(sub)
                    count += 1
                last = sub
                break
        else:
            last = None
        if count == 4:
            break

    result += '0'*(4-count)
    return ''.join(result)

