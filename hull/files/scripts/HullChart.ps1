<#
.SYNOPSIS
    This script performs operations on a HELM chart.
.DESCRIPTION
    This script handles steps to install or test a HELM chart
.PARAMETER HelmChartDirectoryPath
    Path to the directory containing the HELM chart to operate on
.PARAMETER KubeConfigFilePath
    Path to the kubeconfig file for the cluster to install to
.PARAMETER SystemValuesFilePath
    Path to the file containing the system-specific values
.PARAMETER HelmExecutablePath
    Path to the helm executable
.PARAMETER Operation
    The operation to perform on the chart. Supported Values are 'Render' and 'Install'
.PARAMETER ChartNamespace
    The namespace to install the chart into (with Operation 'Install')
.PARAMETER ReleaseName
    The release name of the chart (with Operation 'Install')
.PARAMETER UpdateDependencies
    Whether to run helm dependency update before the operation - NOTE: Only needed when developing and testing the included hull chart
.PARAMETER HullChartDirectoryPath
    Path to the Hull Directory to update dependencies with

.PARAMETER RenderOutputDirectoryPath
    Path to where test output should be rendered (with Operation 'Render')

.EXAMPLE
    C:\PS> ./HullChart.ps1 
        -HelmChartDirectoryPath "C:\helmcharts\scheduling\scheduling-ui\scheduling-ui" 
        -KubeConfigFilePath "C:\helmcharts\scheduling\scheduling-ui\roger-msc-prod.config" 
        -SystemValuesFilePath "C:\helmcharts\scheduling\scheduling-ui\systems\rogers-msc-prod.yaml" 
        -HelmExecutablePath ".\..\..\helm.exe" 
        -Operation "Install"
#>
Param(        
        [string]$KubeConfigFilePath,
        [Parameter(Mandatory=$true)]
        [ValidateSet('Install','Render','Test','Lint')]
        [string]$Operation = "Render",
        [Parameter(Mandatory=$true)]
        [string]$HelmChartDirectoryPath,
        [string]$ChartNamespace,
        [string]$ReleaseName,
        [string]$SystemValuesFilePath,
        [string]$HelmExecutablePath = "helm",
        [bool]$UpdateDependencies = $false,
        [string]$HullChartDirectoryPath = "D:\\GIT\\HULL\\hull",
        [string]$RenderOutputDirectoryPath
    )

# Executes a CMD and interprets exit code
function Execute([string]$cmd)
{
    Write-Verbose "Executing: '$cmd'."
    try {
        [string] $output = ""
        Invoke-Expression -Command $cmd -OutVariable output
        Write-Host $output
        if( $LASTEXITCODE -ne 0 ) 
        {
            throw [Exception]::new("Exit Code was non-zero.")
        }
        Write-Verbose "Executed '$cmd' successfully."
        return $output
    }
    catch {
        throw [Exception]::new("Executing '$cmd' failed")
    }
}

# Get chart name
$chartName = Split-Path $HelmChartDirectoryPath -Leaf

# Set default ReleaseName same as charts name
if ([string]::IsNullOrWhiteSpace($ReleaseName))
{
    $ReleaseName =  $chartName
}

# Set default namespace to KubeConfigFilePath-ReleaseName
if ([string]::IsNullOrWhiteSpace($ChartNamespace))
{
    $ChartNamespace = "$([System.IO.Path]::GetFileNameWithoutExtension($KubeConfigFilePath))-$($ReleaseName)"
}

# Set default systems file to be in a 'systems' folder having the same name as the KubeConfigFilePath
if ([string]::IsNullOrWhiteSpace($SystemValuesFilePath))
{
    $SystemValuesFilePath = [System.IO.Path]::Combine($HelmChartDirectoryPath,"..","systems","$([System.IO.Path]::GetFileNameWithoutExtension($KubeConfigFilePath)).yaml")
}

# Set default render folder
if ([string]::IsNullOrWhiteSpace($RenderOutputDirectoryPath))
{
    $RenderOutputDirectoryPath = [System.IO.Path]::Combine($HelmChartDirectoryPath,"..","test")
}

$helmVersion = 2
# Check if helm runs okay
$helmVersion = Execute "$HelmExecutablePath --kubeconfig $KubeConfigFilePath version"

if ($helmVersion -like "version.BuildInfo{Version:`"v3`.*")
{
    $helmVersion = 3
}
Write-Host "Detected Helm major version: $helmVersion"

$helmSubchartsPath = [System.IO.Path]::Combine($HelmChartDirectoryPath, "charts")
$commonSourceDirectory = [System.IO.Directory]::GetDirectories($helmSubchartsPath) | Where-Object { (Split-Path $_ -Leaf) -like "hull*" } | Select-Object -First 1

if ([String]::IsNullOrWhiteSpace($commonSourceDirectory))
{
    throw [Exception]::new("Failed to find a directory at '" + $helmSubchartsPath + "' starting with 'hull'.")
}

# Update dependencies FOR DEVELOPMENT ONLY of hull
if ($UpdateDependencies)
{
    # Expects the hull library in file:///GIT/HULL/hull otherwise needs adaptation
    # Execute "$HelmExecutablePath dep update --skip-refresh $HelmChartDirectoryPath"

    # Get the created hull-1.0.0.tgz file and the contained version
    # $common = ([System.IO.Directory]::GetFiles([System.IO.Path]::Combine($HelmChartDirectoryPath, "charts")) | Where-Object { [System.IO.Path]::GetFileName($_) -like "hull-1.0.0.tgz"}) | Select-Object -First 1
    $commonVersion = "1.0.0-local"

    # Extract tgz file to charts folder
    # $commonSourceDirectory = [System.IO.Path]::Combine($HelmChartDirectoryPath, "charts")
    # New-Item -ItemType "Directory" -Path "$commonSourceDirectory" -Force
    # Execute "tar -xvzf $common -C $commonSourceDirectory"
    New-Item -ItemType Directory -Path "$([System.IO.Path]::Combine("$($HelmChartDirectoryPath)", "backup", "hull-1.0.0"))" -Force 

    Copy-Item -Path "$([System.IO.Path]::Combine("$($commonSourceDirectory)/*"))" -Destination "$([System.IO.Path]::Combine("$($HelmChartDirectoryPath)", "backup", "hull-1.0.0"))" -Force -Recurse -Exclude @('*.git')
    
    Copy-Item -Path "$($HullChartDirectoryPath)/*" -Destination "$([System.IO.Path]::Combine("$commonSourceDirectory"))" -Force -Recurse -Exclude @('*.git')

    
}
else 
{
    # Regular usage, the hull-1.0.0 library is included as a folder/git submodule
    # $common = ([System.IO.Directory]::GetDirectories([System.IO.Path]::Combine($HelmChartDirectoryPath, "charts")) | Where-Object { (Split-Path $_ -Leaf) -like "hull-1.0.0"}) | Select-Object -First 1
    $commonVersion = "1.0.0-submodule"
    $commonVersionFile = [System.IO.Path]::Combine($HelmChartDirectoryPath, ".git-submodule-hull")
    if ([System.IO.File]::Exists($commonVersionFile))
    {
        $commonVersion = Get-Content -Path $commonVersionFile
    }

    # $commonSourceDirectory = $common
}

# Get the templates to copy to parent chart
foreach ($file in [System.IO.Directory]::GetFiles([System.IO.Path]::Combine($commonSourceDirectory)) | Where-Object {[System.IO.Path]::GetFileName($_) -like "hull_*" }) {
    
    Copy-Item -Path "$file" -Destination "$([System.IO.Path]::Combine($HelmChartDirectoryPath,"templates"))" -Force -Recurse
} 

# Set operation command
$baseOperation = "$HelmExecutablePath  --set-string hull.config.general.metadata.hullLibraryVersion=$commonVersion"
$fullCommand = ""
if ($Operation -eq "Install")
{
    $versionSpecificCommands = if ($helmVersion -eq 3) {"--create-namespace --atomic"} else {""} 
    $fullCommand = "$baseOperation upgrade --install --namespace $ChartNamespace --kubeconfig $KubeConfigFilePath -f $SystemValuesFilePath $versionSpecificCommands $ReleaseName $HelmChartDirectoryPath "
}
elseif ($Operation -eq "Render") {
    $fullCommand = "$baseOperation template  --debug -f $SystemValuesFilePath $HelmChartDirectoryPath --output-dir $RenderOutputDirectoryPath "
}
elseif ($Operation -eq "Lint") {
    $fullCommand = "$baseOperation lint --strict -f $SystemValuesFilePath $HelmChartDirectoryPath "
}

try {
    # Enable debug switch on Verbose or Debug only
    if ($VerbosePreference -eq "Continue" -or $DebugPreference -eq "Continue") {
        $fullCommand += "--debug "
    }
    # Execute Operation on chart
    Execute $fullCommand
}
catch {
    Write-Host "Command failed, cleaning up anyway"
}

# Cleanup the templates folder of parent chart
foreach ($file in [System.IO.Directory]::GetFiles([System.IO.Path]::Combine($HelmChartDirectoryPath,"templates")) | Where-Object {[System.IO.Path]::GetFileName($_) -like "hull_*" }) {
    Remove-Item -Path "$file" -Force -Recurse
} 

# Cleanup in case of development
if ($UpdateDependencies)
{
    # Delete temporary folder for hull chart
    Remove-Item -Path "$commonSourceDirectory/*" -Force -Recurse
    Copy-Item -Path "$([System.IO.Path]::Combine("$HelmChartDirectoryPath", "backup", "hull-1.0.0/*"))" "$([System.IO.Path]::Combine("$commonSourceDirectory"))" -Force 
    Remove-Item -Path "$([System.IO.Path]::Combine("$HelmChartDirectoryPath", "backup", "hull-1.0.0/*"))" -Force -Recurse
    # Delete hull tgz file
    # Remove-Item -Path "$common" -Force
}
