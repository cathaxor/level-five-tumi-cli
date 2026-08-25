$shell = New-Object -ComObject Shell.Application
$folder = $shell.Namespace("F:\Level Five - Tumi")
$file = $folder.ParseName("LEVEL-FIVE-TUMI-Official.mp4")
$duration = $folder.GetDetailsOf($file, 27)
Write-Host "Duration detail: $duration"
