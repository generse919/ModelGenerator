import bpy
def glb2Fbx(glb_path: str, out_fbx_path: str):

    # GLBファイルを指定
    input_glb = glb_path

    # FBXファイルを指定
    output_fbx = out_fbx_path

    # 新しいシーンを作成
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # glTF-Blender-IOアドオンを有効化
    bpy.ops.wm.addon_enable(module='io_scene_gltf')

    # GLBファイルをインポート
    bpy.ops.import_scene.gltf(filepath=input_glb)

    # FBXファイルにエクスポート
    bpy.ops.export_scene.fbx(filepath=output_fbx)

    # Blenderを終了
    bpy.ops.wm.quit_blender()