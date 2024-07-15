import streamlit as st
from diffusers import DiffusionPipeline
import torch

if "image_url" not in st.session_state:
  st.session_state["image_url"] = ""

def create_image(prompt):
    pipe = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16")
    pipe.to("cuda")
    return pipe(prompt=prompt).images[0]

# if using torch < 2.0
# pipe.enable_xformers_memory_efficient_attention()

with st.form("form"):
  prompt = st.text_input("Was solls denn werden?")
  st.form_submit_button("create")
st.session_state.image_url = create_image(prompt)



if st.session_state.image_url != "":
  st.image(st.session_state.image_url)