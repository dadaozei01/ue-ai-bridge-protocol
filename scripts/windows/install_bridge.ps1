param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectDir
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\.."

if (-not (Test-Path -LiteralPath $ProjectDir -PathType Container)) {
    throw "Project directory does not exist: $ProjectDir"
}

$UProjects = @(Get-ChildItem -LiteralPath $ProjectDir -Filter *.uproject -File)
if ($UProjects.Count -eq 0) {
    throw "No .uproject file found directly under: $ProjectDir"
}

New-Item -ItemType Directory -Force -Path "$ProjectDir\Content\Python" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectDir\Saved\CodexScripts" | Out-Null

$PythonDir = "$ProjectDir\Content\Python"
$TaskDir = "$ProjectDir\Saved\CodexScripts"
$InitFile = "$PythonDir\init_unreal.py"

Copy-Item "$RepoRoot\templates\ue5.4\Content\Python\ue_ai_bridge_init.py" "$PythonDir\ue_ai_bridge_init.py" -Force
Copy-Item "$RepoRoot\templates\ue5.4\Content\Python\ue_ai_bridge_runner.py" "$PythonDir\ue_ai_bridge_runner.py" -Force

if (-not (Test-Path -LiteralPath $InitFile -PathType Leaf)) {
    Copy-Item "$RepoRoot\templates\ue5.4\Content\Python\init_unreal.py" $InitFile
} elseif (-not (Select-String -LiteralPath $InitFile -SimpleMatch "UE_AI_BRIDGE_LOADER_START" -Quiet)) {
    Add-Content -LiteralPath $InitFile -Encoding UTF8 -Value @"

# UE_AI_BRIDGE_LOADER_START
import ue_ai_bridge_init  # noqa: F401
# UE_AI_BRIDGE_LOADER_END
"@
}

$TaskScript = "$TaskDir\run_task.py"
if (-not (Test-Path -LiteralPath $TaskScript -PathType Leaf)) {
    Copy-Item "$RepoRoot\templates\ue5.4\Saved\CodexScripts\run_task.py" $TaskScript
} else {
    Write-Host "Preserved existing task script: $TaskScript"
}

Write-Host "Installed UE AI button bridge:"
Write-Host "  $InitFile"
Write-Host "  $PythonDir\ue_ai_bridge_init.py"
Write-Host "  $PythonDir\ue_ai_bridge_runner.py"
Write-Host "  $TaskScript"
Write-Host ""
Write-Host "Restart Unreal Editor once. Then use: 任务脚本 -> 运行任务脚本"
