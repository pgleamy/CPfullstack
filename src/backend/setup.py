import PyInstaller.__main__
import os
    
PyInstaller.__main__.run([  
     '--name=chat_engine.exe',
     '--onefile',
     '-c', # remove -c and change -w to avoid the console window creation
     os.path.join('.', '__main__.py'),                                         
])