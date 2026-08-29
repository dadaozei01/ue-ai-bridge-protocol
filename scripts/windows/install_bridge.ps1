param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectDir
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\.."

New-Item -ItemType Directory -Force -Path "$ProjectDir\Content\Python" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectDir\Saved\CodexScripts" | Out-Null

Copy-Item "$RepoRoot\templates\ue5.4\Content\Python\init_unreal.py" "$ProjectDir\Content\Python\init_unreal.py" -Force
Copy-Item "$RepoRoot\templates\ue5.4\Saved\CodexScripts\run_task.py" "$ProjectDir\Saved\CodexScripts\run_task.py" -Force

Write-Host "Installed UE AI button bridge:"
Write-Host "  $ProjectDir\Content\Python\init_unreal.py"
Write-Host "  $ProjectDir\Saved\CodexScripts\run_task.py"
Write-Host ""
Write-Host "Restart Unreal Editor once. Then use: 任务脚本 -> ▶ 运行任务脚本"
