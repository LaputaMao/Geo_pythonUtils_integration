# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('app.py', '.'), ('scripts', 'scripts'), ('.streamlit', '.streamlit'), ('D:\\miniconda3\\envs\\env\\Lib\\site-packages\\streamlit-1.49.1.dist-info', 'streamlit-1.49.1.dist-info'), ('D:\\miniconda3\\envs\\env\\Lib\\site-packages\\streamlit\\static', 'streamlit/static')],
    hiddenimports=['streamlit.runtime.scriptrunner.magic_funcs', 'natcap.invest'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PythonUtils',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
