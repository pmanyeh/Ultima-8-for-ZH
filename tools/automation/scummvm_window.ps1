# Helper: screenshot / click the ScummVM window (DPI aware). Usage:
#   win.ps1 shot <out.png>
#   win.ps1 dclick <x> <y>     (client coords, physical pixels)
#   win.ps1 click <x> <y>
#   win.ps1 key <SendKeys string>
param([string]$cmd, [string]$a, [string]$b)
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class W {
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
 [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h, ref POINT p);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
 [DllImport("user32.dll")] public static extern void mouse_event(int f, int dx, int dy, int d, int e);
 [DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte scan, int flags, int extra);
 [DllImport("user32.dll")] public static extern uint MapVirtualKey(uint code, uint type);
 public struct RECT { public int L,T,R,B; }
 public struct POINT { public int X,Y; }
}
"@
[W]::SetProcessDPIAware() | Out-Null
$p = Get-Process scummvm -ErrorAction Stop | Select-Object -First 1
$h = $p.MainWindowHandle
[W]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 300
$r = New-Object W+RECT; [W]::GetClientRect($h, [ref]$r) | Out-Null
$o = New-Object W+POINT; [W]::ClientToScreen($h, [ref]$o) | Out-Null
switch ($cmd) {
 'shot' {
  $bmp = New-Object System.Drawing.Bitmap $r.R, $r.B
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($o.X, $o.Y, 0, 0, $bmp.Size)
  $bmp.Save($a); "client {0}x{1}" -f $r.R, $r.B
 }
 { $_ -in 'click','dclick' } {
  [W]::SetCursorPos($o.X + [int]$a, $o.Y + [int]$b) | Out-Null; Start-Sleep -Milliseconds 150
  $n = if ($cmd -eq 'dclick') { 2 } else { 1 }
  for ($i = 0; $i -lt $n; $i++) { [W]::mouse_event(2,0,0,0,0); Start-Sleep -Milliseconds 40; [W]::mouse_event(4,0,0,0,0); Start-Sleep -Milliseconds 80 }
 }
 'key' { [System.Windows.Forms.SendKeys]::SendWait($a) }
 'vk' {  # hardware-style keys with scan codes: "13" (Enter), "17,18,68" (Ctrl+Alt+D)
  $keys = $a.Split(',') | ForEach-Object { [byte][int]$_ }
  foreach ($vk in $keys) { [W]::keybd_event($vk, [byte][W]::MapVirtualKey([uint32]$vk, 0), 0, 0); Start-Sleep -Milliseconds 40 }
  [array]::Reverse($keys)
  foreach ($vk in $keys) { [W]::keybd_event($vk, [byte][W]::MapVirtualKey([uint32]$vk, 0), 2, 0); Start-Sleep -Milliseconds 40 }
 }
}
