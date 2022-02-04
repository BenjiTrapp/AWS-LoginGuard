#!/bin/bash
set -e

readonly SPALSH="""
================================================================================
   ____  _    _         _      _ _            _____ _               _
  / __ \| |  | |  /\   | |    (_) |          / ____| |             | |
 | |  | | |  | | /  \  | |     _| |_ _   _  | |    | |__   ___  ___| | _____
 | |  | | |  | |/ /\ \ | |    | | __| | | | | |    | '_ \ / _ \/ __| |/ / __|
 | |__| | |__| / ____ \| |____| | |_| |_| | | |____| | | |  __/ (__|   <\__\\
  \___\_\\____/_/    \_\______|_|\__|\__, |  \_____|_| |_|\___|\___|_|\_\___/
                                      __/ |
                                     |___/
================================================================================
"""

function banner() {
    printf "$SPLASH"
}

function logQa() {
    echo -e "\e[34mQA -\e[32m $1 \e[0m"
}

function logCodeStyle() {
    echo -e "\e[33mStyle -\e[32m $1 \e[0m"
}

function logSecurity() {
    echo -e "\e[31mSecurity -\e[32m $1 \e[0m"
}

### Security Stuff ###

function runBandit() {
    logSecurity "Security - Running bandit checks"
    bandit -r .
    logSecurity "Done"
}

### Quality Checks ###

function runAllPythonTests() {
    logQa "QA - Running all python tests with coverage"
    coverage run -m unittest discover -s tests
    coverage report 
    if ! test -z "$CREATE_HTML_REPORT" ; then
        logQa "CREATE_HTML_REPORT is set > creating HTML report"
        coverage html
    fi
    logQa "Done"
}

function runAutoPep8() {
    logCodeStyle "Style - Running recursive autopep8"
    autopep8 --in-place --recursive .
    logCodeStyle "Done"
}

function runPyCodeStyle() {
    logCodeStyle "Style - Running pycodestyle"
    pycodestyle --show-source --show-pep8 --max-line-length=1000 .
    logCodeStyle "Done"
}

function runShellCheck() {
    logCodeStyle "Style - Running ShellSheck"
    logCodeStyle "ShellCheck - inspecting argocd-init.sh and argocd-wrapper.sh"
    shellcheck -s bash argocd-init.sh #argocd-wrapper.sh
    for f in ./bin/*.sh
    do  
        [[ "$f" != '*.sh' && -e "$f" ]] || break
        logCodeStyle "ShellCheck - inspecting $f"
        shellcheck -s bash "$f"
    done
    logCodeStyle "Done"
}

### big fucking main ###
function main() {
    banner
    runAllPythonTests
    runBandit
    # runAutoPep8
    runPyCodeStyle
    # runShellCheck
}

# run Forrest run
main