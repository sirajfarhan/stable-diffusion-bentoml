import time
import requests
from urllib.request import urlretrieve
import shutil

from diffusers import StableDiffusionPipeline
import torch

base_url = 'http://54.193.141.160:1337'
model_id = './models/v1_5'


def get_latents(seed, width, height):
    generator = torch.Generator(device='cuda')
    generator = generator.manual_seed(seed)
    return torch.randn(
        (1, pipe.unet.in_channels, height // 8, width // 8),
        generator = generator,
        device = 'cuda')

prompt_reponses = requests.get(base_url + '/api/prompts').json()

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to('cuda')

for prompt_response in prompt_reponses['data']:
    prompt = prompt_response['attributes']['prefix'] + ' sks. ' + prompt_response['attributes']['suffix']
    seed = int(prompt_response['attributes']['seed'])

    width = prompt_response['attributes']['width']
    height = prompt_response['attributes']['height']

    guidance_scale = prompt_response['attributes']['guidance']
    steps = prompt_response['attributes']['steps']

    image = pipe(
        prompt, 
        num_inference_steps=steps, 
        guidance_scale=guidance_scale,
        width=width,
        height=height,
        latents=get_latents(seed, width=width, height=height).half()
    ).images[0]

    image.save('generated.png')

    files = {'files': ('generated.png', open('./generated.png', 'rb'))}
    response = requests.post(base_url + '/api/upload', files=files).json()

    requests.post(
        base_url + '/api/generated-outputs',
        json={
            'data': {
                'generatedImages': [file['id'] for file in response],
                'prompt': prompt_response['id']
            }
        }
    )


