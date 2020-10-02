param (
    [string]$pathmain = "",
    [string]$pathdata = ""
 )
 
$arg = "& 'Q:\Programmes\anaconda\shell\condabin\conda-hook.ps1' ; conda activate edt_env ; python " + $pathmain + "\main.py " + $pathdata 
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -NoExit -Command $arg
