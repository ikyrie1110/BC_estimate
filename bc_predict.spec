# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

xgboost_datas, xgboost_binaries, xgboost_hiddenimports = collect_all('xgboost')

a = Analysis(
    ['bc_predict.py'],
    pathex=[],
    binaries=xgboost_binaries,
    # 关键：把模型文件加入到 datas 中
    datas=xgboost_datas + [
        ('xgb_best_model.pkl', '.'),
        ('feature_names.pkl', '.'),
    ],
    hiddenimports=[
        'sklearn', 'numpy', 'pandas', 'joblib', 'tkinter', 'xgboost'
    ] + xgboost_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BC_Predictor',
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
