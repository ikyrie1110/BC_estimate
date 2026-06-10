# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['bc_predict.py'],          # 你的主脚本文件名
    pathex=[],
    binaries=[],
    datas=[
        ('xgb_best_model.pkl', '.'),
        ('feature_names.pkl', '.'),
    ],
    hiddenimports=[
        'numpy',
        'pandas',
        'xgboost',
        'sklearn',
        'joblib',
        'tkinter',
    ],
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
    name='BC_Estimate',           # 生成的 exe 名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,                  # 显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
