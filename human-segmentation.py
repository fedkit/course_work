import torch
from PIL import Image
import numpy as np
import os

def resize(img, h_new, w_new):
    h, w, c = img.shape
    out = np.zeros((h_new, w_new, c), dtype=np.float32)
    for y in range(h_new):
        sy = y / (h_new - 1) * (h - 1)
        y0 = int(sy)
        y1 = min(y0 + 1, h - 1)
        dy = sy - y0
        for x in range(w_new):
            sx = x / (w_new - 1) * (w - 1)
            x0 = int(sx)
            x1 = min(x0 + 1, w - 1)
            dx = sx - x0
            for ch in range(c):
                out[y,x,ch] = (1-dy)*((1-dx)*img[y0,x0,ch]+dx*img[y0,x1,ch]) + dy*((1-dx)*img[y1,x0,ch]+dx*img[y1,x1,ch])
    return out

folder = './test-photo'
model_path = './models/best_model_java.pt'
save_folder = './test-result'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

model = torch.jit.load(model_path)
model.eval()

for f in os.listdir(folder):
    if not (f.lower().endswith('jpg') or f.lower().endswith('png')):
        continue
    path = os.path.join(folder, f)
    img = Image.open(path).convert('RGB')
    w, h = img.size
    arr = np.array(img).astype(np.float32)/255.0
    arr_r = resize(arr, 512, 512)
    t = torch.tensor(arr_r.transpose(2,0,1)[None,:,:,:])
    with torch.no_grad():
        out = model(t)
    mask = out.squeeze().numpy()
    if mask.ndim==2:
        mask = mask[:,:,None]
    mask = resize(mask, h, w)
    mask = np.clip(mask, 0, 1)

    img_a = np.array(img).astype(np.uint8)
    alpha = (mask[:,:,0]*255).astype(np.uint8)
    img_rgba = np.dstack([img_a, alpha])

    save_path = os.path.join(save_folder, f.rsplit('.',1)[0]+'-person.png')
    Image.fromarray(img_rgba).save(save_path)

