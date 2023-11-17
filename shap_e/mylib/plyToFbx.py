import bpy

# OBJファイルを指定
input_obj = "input.obj"

# FBXファイルを指定
output_fbx = "output.fbx"

# 新しいシーンを作成
bpy.ops.wm.read_factory_settings(use_empty=True)

# OBJファイルをインポート
bpy.ops.import_scene.obj(filepath=input_obj)

# FBXファイルにエクスポート
bpy.ops.export_scene.fbx(filepath=output_fbx)

# Blenderを終了
bpy.ops.wm.quit_blender()
