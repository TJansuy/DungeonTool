#!/usr/bin/env python3

# Imports

from flask import Flask
from flask import send_file
from flask import request

# Init Flask Server
app = Flask(__name__)

# Helper Functions

# Routes

@app.route("/test")
def test():
  return "<p>Your Princess is in another castle</p>"

@app.route("/delayed")
def delayed_response():

    print("args: ",request.args,"\nheaders: ", request.headers,"\norigin: " , request.origin,"\nremote_addr: " ,request.remote_addr)
    import time
    sleep_time = 10
    print("Sleep timer started!", sleep_time,"seconds")
    time.sleep(sleep_time)
    print("Timer done!")

    return send_file("test_image.png", mimetype="image/png")

@app.route("/submit")
def submit_test():
    import base64
    print(request.query_string.decode("ascii"))
    postHash = base64.urlsafe_b64encode(bytes(request.query_string.decode("ascii"), "utf_8"))
    stringHash = postHash.decode("utf_8")
    print("Checking for", stringHash)
    # Check if File Exists
    import os
    if os.path.isfile(stringHash + ".png"):
        print(stringHash, "found")
        return send_file(stringHash + ".png", mimetype="image/png")
    else:
        print("No file exists for", stringHash)
        # No image found
        prompt = request.query_string.decode("ascii")
        generate(stringHash, prompt.replace("query=","").replace("+", " ").replace("%2C",","))
        # Return an image
        return send_file( stringHash + ".png", mimetype="image/png")

# Global lock for atomic operations (Kind of sketchy but functional for now)
lock = False

def generate(filename, positivePrompt, negativePrompt=None):
    # Verify that only one generation happens at a time
    global lock
    if lock is not True:
        lock = True
    else:
        import time
        print("Server busy, waiting")
        while lock is True:
            time.sleep(1) # Sleep for 1 second and check again
        lock = True
        print("Server Ready, starting")

    from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler, StableDiffusionImg2ImgPipeline, StableDiffusionLatentUpscalePipeline
    from diffusers.models import AutoencoderKL
    import torch
    import requests
    # from PIL import Image

    if negativePrompt is None:
        negativePrompt = "blurry"

    guidanceScale = 7
    inferenceSteps = 100

    repo_id = "Ojimi/anime-kawai-diffusion"
    #repo_id = "stabilityai/stable-diffusion-2-1"
    image = False
    
    vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")

    pipe = DiffusionPipeline.from_pretrained(repo_id, vae=vae)
    #pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")
    
    print("Prompt", positivePrompt)
    positivePrompt = "photo anime, masterpiece, high quality" + positivePrompt
    image = pipe(positivePrompt, negative_prompt=negativePrompt, guidance_scale=guidanceScale, num_inference_steps=inferenceSteps, width=448, height=448).images[0]
    #Upscaler
    #image = pipe(positivePrompt, negative_prompt=negativePrompt, guidance_scale=guidanceScale, num_inference_steps=inferenceSteps, width=448, height=448, output_type="latent").images[0]
    
    upscale = False
    if upscale:            
        upscale_repo_id = "stabilityai/sd-x2-latent-upscaler"
        #upscale_repo_id = "stabilityai/stable-diffusion-x4-upscaler"

        upscaler = StableDiffusionLatentUpscalePipeline.from_pretrained(upscale_repo_id, torch_dtype=torch.float16)
        upscaler.to("cuda")
        upscaler.enable_attention_slicing()
        #upscaler.enable_vae_tiling()

        image = upscaler(prompt=positivePrompt, image=image, num_inference_steps=inferenceSteps, guidance_scale=guidanceScale).images[0]


    image.save(filename +".png")
    lock = False
