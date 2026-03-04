# Define the main folder path
$MainFolder = "D:\Cognitive Psychology\Project\img\Ex1"

# Get all JPG files inside subfolders
$Photos = Get-ChildItem -Path $MainFolder -Recurse -Include *.jpg, *.jpeg -File

foreach ($Photo in $Photos) {
    # Build destination path in the main folder
    $Destination = Join-Path $MainFolder $Photo.Name

    # If a file with the same name already exists, add a unique suffix
    if (Test-Path $Destination) {
        $BaseName = [System.IO.Path]::GetFileNameWithoutExtension($Photo.Name)
        $Extension = $Photo.Extension
        $UniqueName = "$BaseName-$([guid]::NewGuid().ToString().Substring(0,8))$Extension"
        $Destination = Join-Path $MainFolder $UniqueName
    }

    # Move the photo to the main folder
    Copy-Item -Path $Photo.FullName -Destination $Destination
}