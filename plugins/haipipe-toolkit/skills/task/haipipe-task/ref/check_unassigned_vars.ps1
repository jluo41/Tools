# Script-scope unassigned-variable check using PowerShell's OWN parser.
# Regex cannot tell a function parameter from a script variable; the AST can.
param([string]$Root)
$auto = @('_','args','null','true','false','PSScriptRoot','PSCommandPath','LASTEXITCODE',
          'PSBoundParameters','Error','Matches','PSItem','host','pwd','HOME','PID','input',
          'foreach','switch','MyInvocation','ErrorActionPreference','ProgressPreference',
          'WarningPreference','OFS','PSVersionTable','ExecutionContext','StackTrace','this')
$findings = 0
Get-ChildItem -Path $Root -Filter *.ps1 -Recurse | ForEach-Object {
    $f = $_.FullName
    $tok = $null; $err = $null
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($f, [ref]$tok, [ref]$err)
    if ($err) { Write-Output "PARSE-ERROR  $f  :: $($err[0].Message)"; $findings++; return }
    # every function body is its own scope; judge SCRIPT scope only
    $funcs = $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst]}, $true)
    $inFunc = { param($n) foreach ($fn in $funcs) { if ($n.Extent.StartOffset -ge $fn.Extent.StartOffset -and $n.Extent.EndOffset -le $fn.Extent.EndOffset) { return $true } } ; return $false }
    $assigned = @{}
    $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.AssignmentStatementAst]}, $true) |
      ForEach-Object { if ($_.Left -is [System.Management.Automation.Language.VariableExpressionAst]) { $assigned[$_.Left.VariablePath.UserPath.ToLower()] = $true } }
    $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.ParameterAst]}, $true) |
      ForEach-Object { $assigned[$_.Name.VariablePath.UserPath.ToLower()] = $true }
    $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.ForEachStatementAst]}, $true) |
      ForEach-Object { $assigned[$_.Variable.VariablePath.UserPath.ToLower()] = $true }
    $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.VariableExpressionAst]}, $true) |
      Where-Object { -not (& $inFunc $_) } |
      ForEach-Object {
        $n = $_.VariablePath.UserPath
        if ($n -match '^(env|script|global|local):') { return }
        if ($auto -contains $n -or $auto -contains $n.ToLower()) { return }
        if (-not $assigned.ContainsKey($n.ToLower())) {
            Write-Output ("UNASSIGNED   {0}:{1}  `${2}" -f (Split-Path -Leaf $f), $_.Extent.StartLineNumber, $n)
            $script:findings++
        }
      }
}
Write-Output "---- $findings finding(s)"
