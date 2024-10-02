import os, argparse
from ds_file.scml import Scml
from ds_file.anim import DSAnim
from ds_file.dyn_decrypt import convert_dyn
from ds_file.image_set import AtlasImages, SpitImage

from ktech.texture_converter import tex_to_png, png_to_tex
from xml.etree.ElementTree import ElementTree

def convert(input_path: str):
    output_path = input_path
    output_path, file_type = os.path.splitext(output_path)
    if file_type != "":
        output_path = os.path.split(output_path)[0]
    print(f"output_path: {output_path}")

    if file_type == ".dyn":
        convert_dyn(input_path)
    elif file_type == ".tex":
        tex_to_png(input_path, output_path)
    elif file_type == ".png":
        png_to_tex(input_path, input_path.replace(".png", ".tex"))
    elif file_type == "":
        root, dirs, files = next(os.walk(output_path), (None, None, []))
        xml_files = [file for file in files if file.find(".xml") != -1]
        png_files = [file for file in files if file.find(".png") != -1]
        dyn_files = [file for file in files if file.find(".dyn") != -1]
        scml_files = [file for file in files if file.find(".scml") != -1]
        zip_files = [file for file in files if file.find(".zip") != -1]

        if xml_files:
            tree_root = ElementTree(file=os.path.join(root, xml_files[0])).getroot()
            if (texture := tree_root.find("Texture")) != None and (name := texture.get("filename")) != None:
                SpitImage(os.path.join(root, xml_files[0]), root, os.path.join(root, name))
                return
        elif png_files:
            AtlasImages(root)
            return
        elif dyn_files:
            for file in dyn_files:
                convert_dyn(os.path.join(root, file))
        elif scml_files:
            for scml_file in scml_files:
                scale = input(f"build {scml_file}, input image scale(default 1):")
                try:
                    scale = float(scale)
                except:
                    scale = 1
                print(f"image scale {scale}")
                Scml(os.path.join(root, scml_file)).build_scml(root, scale)
            return
        elif zip_files:
            mapping = input("input 1 to use symbol mapping(default no)") == "1"
            if mapping:
                print("use symbol mapping")

            anims: list[DSAnim] = []
            for zip_file in zip_files:
                anims.append(DSAnim(os.path.join(root, zip_file)))

            for anim in anims[1:]:
                anims[0] += anim
            anims[0].to_scml(root, mapping=mapping, name=(os.path.splitext(os.path.basename(root))[0] if len(zip_files) > 1 else None))

            for anim in anims:
                anim.close()
            return

    with DSAnim(input_path) as anim:
        anim.convert(output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    args = parser.parse_args()

    convert(args.dir)