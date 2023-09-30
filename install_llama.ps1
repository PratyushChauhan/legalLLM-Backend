# for nvidia gpus on windows only 
python -m venv ./venv
./venv/Scripts/activate
$env:FORCE_CMAKE=1
$env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
pip install llama-index
pip install sentence-transformers
pip install pypdf
pip install docx2txt
pip install websockets