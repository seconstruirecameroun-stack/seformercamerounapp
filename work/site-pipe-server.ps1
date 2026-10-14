param(
  [Parameter(Mandatory = $true)][string]$PipeName,
  [Parameter(Mandatory = $true)][string]$ProjectDir,
  [Parameter(Mandatory = $true)][string]$WorkflowScript,
  [Parameter(Mandatory = $true)][string]$ProjectId
)

$pipe = [System.IO.Pipes.NamedPipeServerStream]::new(
  $PipeName,
  [System.IO.Pipes.PipeDirection]::In,
  1,
  [System.IO.Pipes.PipeTransmissionMode]::Byte,
  [System.IO.Pipes.PipeOptions]::None
)

try {
  $pipe.WaitForConnection()
  $reader = [System.IO.StreamReader]::new($pipe, [System.Text.Encoding]::UTF8)
  $payload = $reader.ReadToEnd()

  $startInfo = [System.Diagnostics.ProcessStartInfo]::new()
  $startInfo.FileName = "node"
  $startInfo.ArgumentList.Add($WorkflowScript)
  $startInfo.ArgumentList.Add("--project-id")
  $startInfo.ArgumentList.Add($ProjectId)
  $startInfo.WorkingDirectory = $ProjectDir
  $startInfo.UseShellExecute = $false
  $startInfo.RedirectStandardInput = $true
  $startInfo.RedirectStandardOutput = $true
  $startInfo.RedirectStandardError = $true

  $process = [System.Diagnostics.Process]::Start($startInfo)
  $process.StandardInput.WriteLine($payload)
  $process.StandardInput.Close()
  $stdout = $process.StandardOutput.ReadToEnd()
  $stderr = $process.StandardError.ReadToEnd()
  $process.WaitForExit()

  if ($stdout) { [Console]::Out.Write($stdout) }
  if ($stderr) { [Console]::Error.Write($stderr) }
  exit $process.ExitCode
}
finally {
  if ($reader) { $reader.Dispose() }
  $pipe.Dispose()
}
