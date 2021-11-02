# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\Owner\\Documents\\GitHub\\Image-Editor-Python\\src\\main\\python\\main.py'],
             pathex=['C:\\Users\\Owner\\Documents\\GitHub\\Image-Editor-Python\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['c:\\users\\owner\\appdata\\local\\programs\\python\\python36\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['C:\\Users\\Owner\\Documents\\GitHub\\Image-Editor-Python\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='MyFbsApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , version='C:\\Users\\Owner\\Documents\\GitHub\\Image-Editor-Python\\target\\PyInstaller\\version_info.py', icon='C:\\Users\\Owner\\Documents\\GitHub\\Image-Editor-Python\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='MyFbsApp')
