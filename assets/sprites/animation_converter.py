from PIL import Image
import os
''' Instruções:
1. Ajuste o nome
2. Coloque os spritesheets na pasta assets/sprites/enemies/{name}
3. Nomeie os arquivos como {name}_{state}_with_shadow.png
'''
# Configurações
name = "campfire"
frame_width = 32   # ajuste conforme o tamanho do frame
frame_height = 64
rows = 1
cols = 8
directions = [""]
states = ["starting", "burning"]

output_dir = f"assets/sprites/details/{name}"

for s in states:
    state_dir = os.path.join(output_dir, s)
    os.makedirs(state_dir, exist_ok=True)
    
    img = Image.open(f"{output_dir}/{name}_{s}.png")
    cols = img.width // frame_width
    
    for r in range(rows):
        direction = directions[r]
        for c in range(cols):
            frame = img.crop((
                c * frame_width,
                r * frame_height,
                (c + 1) * frame_width,
                (r + 1) * frame_height
            ))
            path = f"{state_dir}/{direction}_{c+1}.png"
            frame.save(path)
    
    os.remove(f"{output_dir}/{name}_{s}.png")
print("Animações convertidas e salvas com sucesso!")
