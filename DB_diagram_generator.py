import os
import subprocess
from eralchemy import render_er
from src.DB.startup import SQLModel

def main():
    if os.path.exists('ERD.png'):
        os.remove('ERD.png')
    render_er(SQLModel.metadata, 'erd.dot')
    subprocess.run(['dot', '-Tpng', 'erd.dot', '-o', 'ERD.png'])
    os.remove('erd.dot')


if __name__ == '__main__':
    main()