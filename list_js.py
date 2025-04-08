import os
import json

def new_q():
    folder = 'questions'
    files = sorted([f for f in os.listdir(folder) if f.startswith('plot') and f.endswith('.png') and f[4:-4].isdigit() and int(f[4:-4]) >= 100])
    with open(os.path.join(folder, 'list.json'), 'w', encoding='utf-8') as f:
        json.dump(files, f, indent=2)

if __name__ == '__main__':
    new_q()