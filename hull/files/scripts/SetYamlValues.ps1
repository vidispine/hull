<#
.SYNOPSIS
    This script sets simple values in a YAML file    
.PARAMETER YamlFilePath
    Path to the directory containing the HELM chart to operate on
.PARAMETER Overwrites
    Specify additional keys that should be overwritten with given values.
    For each pair, the keys and values are seperated by the AdditionalOverwritesSplitChar (defaults to '=')
    Key value pairs are seperated by two AdditionalOverwritesSplitChar '=='. 
    If key or value can contain AdditionalOverwritesSplitChar, make sure to escape it before input like '\='.
    Specify like this:

    <key1>=<value1>=<key2>=<value2>
    
    In consequence an equal number of entries must be input. Change the AdditionalOverwritesSplitChar if needed.
.PARAMETER OverwritesSplitChar
    Specify the split character for the AdditionalOverwrites


.EXAMPLE
    C:\PS> ./SetYamlValues.ps1 
        -YamlFilePath "c:\\git\\MediaEditor\\helm\\mediaeditor\\values.yaml"
        -Overwrites "hull.object.deployments.mediaeditor.pod.containers.mediaeditor.image=xxx"
#>


Param(        
        [Parameter(Mandatory=$true)]
        [string]$YamlFilePath,
        [string]$Overwrites = "",
        [string]$OverwritesSplitChar = '='
    )

    
Import-Module powershell-yaml

$replacements = @{}


if ([String]::IsNullOrWhiteSpace($Overwrites))
{
  Write-Host "Nothing to Set specified in Overwrites."
  return
}
else
{
    if ($Overwrites.Contains("\$($OverwritesSplitChar)"))
    {
        throw [NotImplementedException]::new("Escaping not implemented yet.")
    }

    $overwrite = $Overwrites.Split($OverwritesSplitChar, [System.StringSplitOptions]::RemoveEmptyEntries)
    for ($i = 0; $i -lt $overwrite.Length; $i++)
    {        
        if ($i % 2 -eq 0)
        {
            $key = $($overwrite[$i].Split('.')[$overwrite[$i].Split('.').Length - 1])
            $replacements.Add($overwrite[$i], @{ 
                "type" = "keyValueOverwrite"
                "parentKey" = [Regex]::Replace($overwrite[$i], "\.?$($key)\s*$", "")
                "key" = $key
                "value" = $overwrite[++$i]
            })    
        }
    }
}

# Iterate image tag paths
foreach ($replacementKey in $replacements.Keys) {

    Write-Host "SetYamlValues: Currently processing '$replacementKey' ..."
    $entry = $replacements[$replacementKey].parentKey
    # Gets values yaml as string array
    $valuesString = (Get-Content $YamlFilePath)
    
    # Get all keys from dot notation
    $processed = @()   
    $keys = $entry.Split('.', [System.StringSplitOptions]::RemoveEmptyEntries)
    $keysCount = $keys.Count
    $keysCounter = 0
    $whitespaceCount = 0
    $atRootLevel = $keysCount -eq 0
    $currentKey = $keys[$keysCounter]
    $padding = if($atRootLevel) {0} else {2}
    $found = $false
    for ($line = 0; $line -lt $valuesString.Length + 1; $line++) 
    {
           

        if($atRootLevel)
        {
            $currentLine = $valuesString[$line]        

            # If key is already present overwrite later
            if (($currentLine -cmatch "(^|\s+)$($replacements[$replacementKey].key):\s+" -or $line -ge ($valuesString.Length)) -and !$found)
            {
                $key = $replacements[$replacementKey].key
                $value = $replacements[$replacementKey].value
                $exchanged = "$($key): $($value)"
                Write-Host "SetYamlValues: Exchanged this: '$exchanged' ..."
                $processed += [PSObject]($exchanged.PadLeft($exchanged.Length + $whitespaceCount + $padding))
                $found = $true
            }
            else
            {
                if ($line -lt ($valuesString.Length))
                {
                    $processed += ($currentLine)           
                }
            }
        }
        else 
        {
            # Simple approach to preserve comments in YAML
            # which are lost by serialization
            # When current key is found set next key to be matched
            if ($line -ge $valuesString.Length)
            {
                break;
            }
            $currentLine = $valuesString[$line]        
            if ($currentLine -cmatch "(^|\s+)$($currentKey):\s*")
            {
                # Matched all keys                 
                if ((($keysCount - 1) -eq $keysCounter))
                {
                    # Remember indentation
                    $whitespaceCount = 0
                    
                    $whitespaceCount = $currentLine.Length - $currentLine.TrimStart(' ').Length
                    $processed += ($currentLine)                    

                    # Now check the existing fields and decide to keep them or ignore them
                    while ($true)
                    {
                        $line++;
                        $currentLine = $valuesString[$line]  
                        
                        if ($replacements[$replacementKey].type -eq "keyValueOverwrite")
                        { 
                            # If indentation is greater than for metadata: tag it is a sub key to be copied
                            if ((($currentLine.Length - $currentLine.TrimStart(' ').Length -gt $whitespaceCount)))
                            {
                                # If tag is already present for some reason in product values.yaml we just overwrite it later
                                if ($currentLine -cmatch "(^|\s+)$($replacements[$replacementKey].key):\s+")
                                {
                                # Skip line 
                                }
                                else
                                {
                                    $processed += ($currentLine)
                                }
                            }
                            else 
                            {
                                $key = $replacements[$replacementKey].key
                                $value = $replacements[$replacementKey].value
                                $exchanged = "$($key): $($value)"
                                Write-Host "SetYamlValues: Exchanged this: '$exchanged' ..."                
                                $processed += [PSObject]($exchanged.PadLeft($exchanged.Length + $whitespaceCount + $padding))

                                # Emit buffered line
                                if ($null -ne $currentLine)
                                {
                                    $processed += ($currentLine)  
                                }
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
        
    }

    Set-Content -Path "$($YamlFilePath)" -Value ($processed)
}
