import GPUtil
import os
from shap_e.diffusion.sample import sample_latents
from shap_e.util.image_util import load_image
from shap_e.util.notebooks import decode_latent_mesh
import tempfile
import torch
import trimesh
import numpy as np
from shap_e.mylib.glbToFbx import glb2Fbx

def to_glb(ply_path: str, output_path: str):
    print("to_glb: " + output_path + "ply: " + ply_path)
    mesh = trimesh.load(ply_path)
    rot = trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0])
    mesh = mesh.apply_transform(rot)
    rot = trimesh.transformations.rotation_matrix(np.pi, [0, 1, 0])
    mesh = mesh.apply_transform(rot)
    # mesh_path = tempfile.NamedTemporaryFile(suffix=".glb", delete=False)
    mesh.export(output_path, file_type="glb")



def model_create(xm,model,diffusion,imgPath:str,batch_size = 1, guidance_scale = 3.0, inference_steps = 64):


    # To get the best result, you should remove the background and show only the object of interest to the model.
    image = load_image(imgPath)
    srcdata = imgPath.replace('Assets/example_data/', '').removesuffix('.png').removesuffix('.jpg')
    print(f'loaded: {srcdata}')
    dir = 'Assets/model_' + srcdata
    if not os.path.exists(dir):
        os.mkdir(dir)
    print(f'makeModel: {srcdata}')
    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(images=[image] * batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=inference_steps,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )
    
    GPUtil.showUtilization()
    print(f'write models: {srcdata}')
    for i, latent in enumerate(latents):
        t = decode_latent_mesh(xm, latent).tri_mesh()


        ply_path = tempfile.NamedTemporaryFile(suffix=".ply", delete=False, mode="w+b")
        glb_path = tempfile.NamedTemporaryFile(suffix=".glb", delete=False, mode="w+b")
        output_path = f'{dir}/output.fbx'
        
        with open(ply_path.name, 'wb') as f:
            t.write_ply(f)
        to_glb(ply_path.name,glb_path.name)
        torch.cuda.empty_cache()
        glb2Fbx(glb_path.name, output_path)
    GPUtil.showUtilization()
    


    del latents