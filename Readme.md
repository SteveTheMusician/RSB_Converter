# RSB Image Converter
## Installs
- install python 3
- install pillow via "pip install pillow" in terminal (admin)

## run script
- Convert RSP to Png: "python {PATH_TO_THE_PYTHON_FILE}\rsb_converter.py to_png {PATH_TO_RSB_FILE}\{YOUR_FILE}.rsb {OUTPUT_FOLDER_NAME}"
- - Example: "python C:\Users\User\Downloads\rsb_converter.py to_png C:\Users\User\Downloads\menu.rsb converted_image"
- Convert PNG to rsb: "python {PATH_TO_THE_PYTHON_FILE}\rsb_converter.py to_rsb {PATH_TO_PNG_FILE}\{YOUR_FILE}.png {OUTPUT_FILE_NAME}.rsb"
- - Example: "python C:\Users\User\Downloads\rsb_converter.py to_rsb C:\Users\User\Downloads\menu.png menu.rsb"

Important: To convert your file back to rsb, you have to put the meta-file, which you got from the extraction beefore, next to it.
Otherwise the proccess will fail

----

!! Currently u can only use the rsb_converter.py in the src folder (its working fine) - UI Version is comming soon
