# تشغيل مختبر الاقتصاد الكلي المعمّق محليًا
# 1) المحاكي (Streamlit) على :8508
# 2) قشرة PWA على :8000  → افتح http://localhost:8000 في المتصفح

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

Write-Host "⏳ بدء تشغيل المحاكي (Streamlit) على المنفذ 8508..." -ForegroundColor Cyan
$proc = Start-Process python -ArgumentList @(
    "-m", "streamlit", "run", "app.py",
    "--server.port", "8508",
    "--server.address", "localhost"
) -WorkingDirectory $root -PassThru -WindowStyle Hidden

Start-Sleep -Seconds 6

Write-Host "⏳ بدء قشرة PWA على المنفذ 8000..." -ForegroundColor Cyan
$pwa = Start-Process python -ArgumentList @(
    "serve_pwa.py", "--port", "8000"
) -WorkingDirectory $root -PassThru -WindowStyle Hidden

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✨ التطبيق جاهز!" -ForegroundColor Green
Write-Host "   افتح : http://localhost:8000" -ForegroundColor Yellow
Write-Host "   (المحاكي المباشر: http://localhost:8508)" -ForegroundColor DarkGray
Write-Host ""
Write-Host "لإيقاف كل شيء:  Stop-Process -Id $($proc.Id),$($pwa.Id) -Force"

Start-Process "http://localhost:8000"

# انتظر إغلاق العمليات (سطر أوامر تفاعلي)
try {
    while (-not $proc.HasExited -and -not $pwa.HasExited) { Start-Sleep -Seconds 2 }
} finally {
    if (-not $proc.HasExited) { Stop-Process -Id $proc.Id -Force }
    if (-not $pwa.HasExited) { Stop-Process -Id $pwa.Id -Force }
}