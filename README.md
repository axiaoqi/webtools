# webtools
一些实用功能整理




## requirments
python=3.9

```bash
pip install flask requests spark_ai_python

cd cnquant
pip install -e .
```


## 打包为单位件pywebview

```bash
pyinstaller --name "我的工具箱" --windowed --onefile --icon="static/favicon.ico" main_ui_pywebview.py
```

```bash
pyinstaller --name "我的工具箱" --onefile --icon="static/favicon.ico" main_ui_pywebview.py
```

```bash
pyinstaller --name "我的工具箱" ^
--windowed ^
--onefile ^
--icon="static/favicon.ico" ^
--add-data "templates;templates" ^
--add-data "static;static" ^
main_ui_pywebview.py
```