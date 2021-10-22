<#
.SYNOPSIS
    This script sets a version to a Helm chart
.DESCRIPTION
    This script sets a version to a Helm chart by changing the Chart.yaml and dedicated image tags in the values.yaml
.PARAMETER HelmChartDirectoryPath
    Path to the directory containing the HELM chart to operate on
.PARAMETER Version
    Version to set in Chart.yaml fields 'appVersion' and 'version' and the image tags specified under 'ProductImages'
.PARAMETER ProductImages
    Semicolon-delimited string containing information about the images for which the version is to be replaced in values.yaml.
    Each entry consists of one, two or three segments which are then themselves delimited by ':'.
    If only one segment exists, it represents the YAML Path to the 'image:' tag which should be overwritten in dot-notation
    If two or three segments exist:
    - the first segment represents the YAML Path to the 'image:' tag which should be overwritten in dot-notation
    - the second or third segment needs to start with either 'REGISTRY=' or 'REPOSITORY=' to indicate the registry or repository to overwrite    
.PARAMETER HullVersion
    The version of the hull library to set in object metadata.
.PARAMETER AdditionalOverwrites
    Specify additional keys that should be overwritten with given values.
    For each pair, the keys and values are seperated by the AdditionalOverwritesSplitChar (defaults to '=')
    Key value pairs are seperated by AdditionalOverwritesSplitChar too. 
    If key or value can contain AdditionalOverwritesSplitChar, make sure to escape it before input like '\='.
    Specify like this:

    <key1>=<value1>=<key2>=<value2>
    
    In consequence an equal number of entries must be input. Change the AdditionalOverwritesSplitChar if needed.
.PARAMETER AdditionalOverwritesSplitChar
    Specify the split character for the AdditionalOverwrites


.EXAMPLE
    C:\PS> ./SetChartVersion.ps1 
        -Version "20.1.1-alpha" 
        -HelmChartDirectoryPath "c:\\git\\MediaEditor\\helm\\mediaeditor\\"
        -ProductImages "hull.object.deployments.mediaeditor.pod.containers.mediaeditor.image"
#>


Param(        
        [Parameter(Mandatory=$true)]
        [string]$HelmChartDirectoryPath,
        [Parameter(Mandatory=$true)]
        [string]$Version,
        [string]$ProductImages,
        [string]$HullVersion,
        [string]$AdditionalOverwrites,
        [string]$AdditionalOverwritesSplitChar = '='
    )

    
Import-Module powershell-yaml

# Paths to relevant files
$chartYamlPath = [System.IO.Path]::Combine($HelmChartDirectoryPath, "Chart.yaml")
$valuesYamlPath = [System.IO.Path]::Combine($HelmChartDirectoryPath, "values.yaml")

# Change Chart.yaml fields
$cmd = "$([System.IO.Path]::Combine($PSScriptRoot, "SetYamlValues.ps1")) -YamlFilePath '$chartYamlPath' -Overwrites 'appVersion=$Version==version=$Version'"
Invoke-Expression -Command $cmd
  
# Determine all product images to be changed
$images = $ProductImages.Split(';')
$replacements = @{}

foreach ($image in $images) {

    $split = $image.Split(':')

    # Add custom repository
    $repository = $null
    $registry = $null

    if ($split.Length -gt 1)    
    {
        for ($i = 1; $i -lt $split.Length; $i++)
        {
            if ($split[$i].StartsWith("REGISTRY="))
            {
                $registry = $split[$i].Substring("REGISTRY=".Length)
            }
            elseif ($split[$i].StartsWith("REPOSITORY="))
            {
                $repository = $split[$i].Substring("REPOSITORY=".Length)
            }
            else
            {
                if ($split.Length -eq 2)
                {
                    $registry = $split[$i]
                }
            }
        }   
    }

    $replacements.Add(
        $split[0], @{
            "type" = "productImage" 
            "repository" = $repository
            "registry" = $registry
            "tag" = $Version
        }     
    )
}

# Iterate image tag paths
foreach ($entry in $replacements.Keys) {

    # Gets values yaml as string array
    Write-Host "Currently processing '$entry' ..."
    $valuesString = (Get-Content $valuesYamlPath)
    
    # Get all keys from dot notation
    $processed = @()   
    $keys = $entry.Split('.')
    $keysCount = $keys.Count
    $keysCounter = 0
    $currentKey = $keys[$keysCounter]
    
    for ($line = 0; $line -lt $valuesString.Length; $line++) {
        
        $currentLine = $valuesString[$line]           

        # Simple approach to preserve comments in YAML
        # which are lost by serialization
        # When current key is found set next key to be matched
        if ($currentLine -match "^\s*$($currentKey):\s*")
        {
            Write-Host "Current line '$($currentLine)' matched pattern '^\s*$($currentKey):\s*'"
            # Matched all keys                 
            if (($keysCount - 1) -eq $keysCounter)
            {
                # Remember indentation
                $whitespaceCount = $currentLine.Length - $currentLine.TrimStart(' ').Length
                $processed += ($currentLine)

                # Now check the existing fields and decide to keep them or ignore them
                while ($true){
                    
                    $line++;
                    $currentLine = $valuesString[$line]  

                    if ($replacements[$entry].type -eq "productImage")
                    {
                        # If indentation is greater than for image: tag it is a sub key to be handled
                        if ($currentLine.Length - $currentLine.TrimStart(' ').Length -gt $whitespaceCount)
                        {
                            # If not overwritten keep repository tag 
                            if ($currentLine.Contains("repository:") -and $null -eq $replacements[$entry].repository)
                            {
                                Write-Host "Keeping current line's '$($currentLine)' repository, it is not overwritten"
                                $processed += ($currentLine)   
                            }
                            if ($currentLine.Contains("registry:") -and $null -eq $replacements[$entry].registry)
                            {
                                Write-Host "Keeping current line's '$($currentLine)' registry, it is not overwritten"
                                $processed += ($currentLine)   
                            }
                        }
                        else 
                        {
                            # Overwrite repository if specified
                            if ($null -ne $replacements[$entry].repository)
                            {
                                $repo = "repository: $($replacements[$entry].repository)"
                                Write-Host "Overwriting repository: with '$($repo)'"
                                $processed += [PSObject]($repo.PadLeft($repo.Length + $whitespaceCount + 2))
                            }

                            if ($null -ne $replacements[$entry].registry)
                            {
                                $repo = "registry: $($replacements[$entry].registry)"
                                Write-Host "Overwriting registry: with '$($repo)'"
                                $processed += [PSObject]($repo.PadLeft($repo.Length + $whitespaceCount + 2))
                            }

                            # Set tag to version
                            $tag = "tag: $($replacements[$entry].tag)"
                            Write-Host "Setting tag: to '$($tag)'"
                            $processed += [PSObject]($tag.PadLeft($tag.Length + $whitespaceCount + 2))

                            # Emit buffered line
                            $processed += ($currentLine)
                            
                            break;
                        }
                    }                    
                }
                
                # Reset current key
                $keysCounter = 0
                $currentKey = $keys[$keysCounter]
            }
            else 
            {
                $processed += ($currentLine)  
                $currentKey = $keys[++$keysCounter]  
            }
            
        }
        else 
        {
            
            $processed += ($currentLine)
        }
    }
    
    Write-Host "Done processing '$entry' ..."
    Set-Content -Path "$($valuesYamlPath)" -Value ($processed)
    
    $overwrites = ""
    if (![String]::IsNullOrWhiteSpace($AdditionalOverwrites))
    {
        $overwrites += $AdditionalOverwrites
    }
    
    $cmd = "$([System.IO.Path]::Combine($PSScriptRoot, "SetYamlValues.ps1")) -YamlFilePath '$valuesYamlPath' -Overwrites '$overwrites' -OverwritesSplitChar '$AdditionalOverwritesSplitChar'"
    Invoke-Expression -Command $cmd
}

if (![String]::IsNullOrWhiteSpace($HullVersion))
{
    $processed = @()  
    $valuesString = (Get-Content $valuesYamlPath)
    for ($line = 0; $line -lt $valuesString.Length; $line++) {
        $currentLine = $valuesString[$line]
        if ($currentLine -match "^hull:\s*")
        {
            Write-Host "Found hull: '$($entry)' ..."
            $processed += $currentLine

            $nextLine = $valuesString[$line+1]
            if ($nextLine -match "  version: " + $HullVersion)
            {
                Write-Host "Hull version already set to 'version: + $($HullVersion)'"
            }
            else
            {
                Write-Host "Setting Hull version to 'version: + $($HullVersion)'"
                $processed += ("  version: " + $HullVersion)
            }
        }
        else
        {
            $processed += $currentLine
        }
    }
    Set-Content -Path "$($valuesYamlPath)" -Value ($processed)
}


