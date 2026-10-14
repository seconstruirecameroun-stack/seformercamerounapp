param([Parameter(Mandatory = $true)][string]$PipeName)

$pipe = [System.IO.Pipes.NamedPipeClientStream]::new(
  ".",
  $PipeName,
  [System.IO.Pipes.PipeDirection]::Out,
  [System.IO.Pipes.PipeOptions]::None
)

try {
  $pipe.Connect(30000)
  $payload = [Console]::In.ReadToEnd()
  $writer = [System.IO.StreamWriter]::new($pipe, [System.Text.UTF8Encoding]::new($false))
  $writer.Write($payload)
  $writer.Flush()
}
finally {
  if ($writer) { $writer.Dispose() }
  $pipe.Dispose()
}
