# -*- mode: python -*-

block_cipher = None


a = Analysis(['Gui.py'],
             pathex=['C:\\Users\\ogunk\\Documents\\code\\SameGame'],
             binaries=[],
             datas=[('Fonts','Fonts'),('TopScores.txt','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Gui',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
         name='Bantu.app',
         icon='same.ico',
         bundle_identifier=None,
         info_plist={
            'NSHighResolutionCapable': 'True'
            },
         )
