# Dashboard Financeiro - Servidor 24/7
# Este script reinicia automaticamente o servidor se ele cair

$ProjectDir = "c:\Users\GabrielOliveiraDeFar\OneDrive - Argus Solutions\Gabriel\analise-contas"
$LogFile = Join-Path $ProjectDir "server_24_7.log"
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"

function Log-Message {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$Timestamp] $Message"
    Write-Host $LogMessage
    Add-Content -Path $LogFile -Value $LogMessage
}

Write-Host "`n============================================"
Write-Host "DASHBOARD FINANCEIRO - SERVIDOR 24/7"
Write-Host "============================================`n"

Log-Message "Iniciando servidor 24/7"

while ($true) {
    try {
        Log-Message "Iniciando processo Flask..."
        
        $Process = Start-Process -FilePath $PythonExe `
                                -ArgumentList "servidor_dash.py" `
                                -WorkingDirectory $ProjectDir `
                                -PassThru `
                                -NoNewWindow
        
        Log-Message "Servidor iniciado (PID: $($Process.Id))"
        
        # Aguardar até o processo terminar
        $Process.WaitForExit()
        
        Log-Message "AVISO: Servidor foi interrompido (exit code: $($Process.ExitCode))"
        Log-Message "Aguardando 5 segundos antes de reiniciar..."
        
        Start-Sleep -Seconds 5
    }
    catch {
        Log-Message "ERRO: $_"
        Start-Sleep -Seconds 5
    }
}
