import bpy

# blender側のPythonから実行する必要がある。

def _glb2FbxInternal(glb_path: str, out_fbx_path: str):

    # GLBファイルを指定
    input_glb = glb_path

    # FBXファイルを指定
    output_fbx = out_fbx_path

    # 新しいシーンを作成
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # glTF-Blender-IOアドオンを有効化
    bpy.ops.preferences.addon_enable(module='io_scene_gltf2')

    # GLBファイルをインポート
    bpy.ops.import_scene.gltf(filepath=input_glb)

    # FBXファイルにエクスポート
    bpy.ops.export_scene.fbx(filepath=output_fbx)

    # Blenderを終了
    bpy.ops.wm.quit_blender()


import sys
import argparse

def main(argv):
    #blender側Pythonで実行するとき、引数は文字列としてパースをする必要があるため、直す。
    parser = argparse.ArgumentParser()
    parser.add_argument('--glb_path', type=str, required=True,
        help='glb_path: glbファイルのパス')
    parser.add_argument('--out_fbx_path', type=str, required=True,
        help='out_fbx_path: FBX出力先のパス')

    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    glb_path = str(args.glb_path)
    out_fbx_path = str(args.out_fbx_path)

    print(f"glb_path = {glb_path}, output_path = {out_fbx_path}")

    _glb2FbxInternal(glb_path, out_fbx_path)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))