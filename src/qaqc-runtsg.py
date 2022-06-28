import subprocess

cmd = '.\\tsgeol8.exe /script=script.txt'
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
process.wait()
print('>>nvcl-qaqc:run tsgscript:'+ cmd)

cmd = '.\\tsgeol8.exe /script=20210818_2Bstd_standardise.txt'
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
process.wait()
print('>>nvcl-qaqc:run tsgscript:'+ cmd)

cmd = '.\\tsgeol8.exe /script=20210818__2Bstd_wvlcal_TIR.txt'
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
process.wait()
print('>>nvcl-qaqc:run tsgscript:'+ cmd)

cmd = '.\\tsgeol8.exe /script=20210908_2Bstd_puckwcal_testrox_wvlcal(no2206)_GSWA.txt'
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
process.wait()
print('>>nvcl-qaqc:run tsgscript:'+ cmd)


print('>>nvcl-qaqc:finished!')
