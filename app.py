import gradio as gr
import json

with open('pokemon.json', 'r') as f:
    pokemons = json.load(f)

GEN_RANGE = {
    "1세대": [1, 151],
    "2세대": [152, 251],
    "3세대": [252, 386],
    "4세대": [387, 493],
    "5세대": [494, 649],
    "6세대": [650, 721],
    "7세대": [722, 809],
    "8세대": [810, 898],
    "9세대": [899, 1017]
}

generation = gr.Dropdown(
            [f"{k}세대" for k in range(1, 10)], value="1세대", label="포켓몬 세대", info="원하는 포켓몬 세대를 선택하세요."
        )

download = gr.File(label="Download a file")

def run(gen):
    results = []
    start, end = GEN_RANGE[gen]
    for k in range(start, end+1):
        results.append(pokemons[k-1]['name'])
    return "\n".join(results)

demo = gr.Interface(run, generation, "text")
demo.queue()
demo.launch(share=True)