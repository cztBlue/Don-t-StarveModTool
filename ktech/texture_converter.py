import os, sys
import subprocess

TOOL_PATH = os.path.dirname(__file__)
KTECH = os.path.abspath(os.path.join(TOOL_PATH, "ktech.exe"))
TEXTURE_CONVERTER = os.path.abspath(os.path.join(TOOL_PATH, "TextureConverter.exe"))

def tex_to_png(input_paths: list[str]|str, output: str):
    if isinstance(input_paths, str):
        input_paths = [input_paths]

    for input_path in input_paths:
        cmd_list = [KTECH, input_path, output]
        if subprocess.call(cmd_list) != 0:
            sys.stderr.write("Error attempting to convert {} to {}\n".format(input_path, output))

def png_to_tex(input_paths: list[str]|str, output: str, texture_format="bc3", no_premultiply=False, platform="opengl",
            generate_mips=False, width=None, height=None, verbose=False, ignore_exceptions=False):

    if isinstance(input_paths, str):
        input_paths = [input_paths]

    # If a list is passed in, concatenate the filenames with semi-colon separators, otherwise just use the filename
    src_filename_str = ';'.join(input_paths)

    cmd_list = [TEXTURE_CONVERTER,
        '--swizzle',
        '--format ' + texture_format,
        '--platform ' + platform,
        '-i ' + src_filename_str,
        '-o ' + output,
    ]

    if generate_mips:
        cmd_list.append('--mipmap')

    if not no_premultiply:
        cmd_list.append('--premultiply')

    if width:
        cmd_list.append('-w {}'.format(width))
    if height:
        cmd_list.append('-h {}'.format(height))

    cmd = " ".join(cmd_list)
    if verbose:
        print(cmd)
    if subprocess.call(cmd_list) != 0:
        sys.stderr.write("Error attempting to convert {} to {}\n".format( input_paths, output))
        sys.stderr.write(cmd + "\n")
        if not ignore_exceptions:
            raise