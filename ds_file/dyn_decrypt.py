"""
The MIT License (MIT)

Copyright (c) 2020 Wessel "PassTheWessel" T <discord@go2it.eu>
Copyright (c) 2021 UNOWEN-OwO

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# https://github.com/UNOWEN-OwO/dyn_decrypt/blob/master

import os

def convert_dyn(filename, debug_info=False):
    print("convert_dyn" + filename)

    def debug(msg):
        if debug_info:
            print(msg)

    dest = os.path.splitext(filename)[0] + (".zip" if (isDecrypt := os.path.splitext(filename)[1] == ".dyn") else ".dyn")

    # XOR key and shuffle index arrays for convert
    CHUNK_SIZE = 8
    key = bytearray([(0x8D + i) for i in range(CHUNK_SIZE)])
    indices = [5, 3, 6, 7, 4, 2, 0, 1]

    debug("chunk size = {}, key = {}, indices = {}".format(CHUNK_SIZE, key, indices))
    debug("filename = {}, dest = {}".format(filename, dest))

    with open(filename, "rb") as file, open(dest, "wb") as output:
        swap = 0
        while (swap := swap + 1) > 0:
            # Read in a chunk of raw data
            chunk = (file.read(CHUNK_SIZE) if swap == 1 else chunk[CHUNK_SIZE:]) + file.read(CHUNK_SIZE)
            if not chunk or (swap == 1 and isDecrypt and chunk[:2] == b"PK"):
                output.write(chunk + file.read() + b""[:(swap := -2)] if swap == 1 and chunk[:2] == b"PK" else b""[:(swap := -1)])

            else:  # Need a full 8-byte chunk to convert.
                if len(chunk) > CHUNK_SIZE:
                    out = bytearray(CHUNK_SIZE)

                    # Convert the chunk.
                    for i in range(CHUNK_SIZE):
                        out[i if isDecrypt else indices[i]] = chunk[indices[i] if isDecrypt else i] ^ key[i]
                else:
                    out = chunk

                debug("out = {}".format(out))
                output.write(out)

        print("{} {} to {}".format("Decrypted" if isDecrypt else "Encrypted", filename, dest) if not swap else "IT IS A ZIP!")