; Ctrl+Shift+R: copy selection, convert to ruby HTML, paste back.
#NoEnv
#SingleInstance Force
SetWorkingDir %A_ScriptDir%

^+r::
    ClipSaved := ClipboardAll
    Clipboard := ""
    Send ^c
    if !ClipWait(1) {
        MsgBox, 48, Convert Selection, No text selected.
        Clipboard := ClipSaved
        return
    }

    RunWait, "%A_ScriptDir%\.venv\Scripts\python.exe" "%A_ScriptDir%\convert_selection.py" --clipboard,, Hide
    if ErrorLevel {
        MsgBox, 48, Convert Selection, Conversion failed. Use format: 中文（English） or 中文（English，ABBR）
        Clipboard := ClipSaved
        return
    }

    Send ^v
    Sleep 100
    Clipboard := ClipSaved
return
