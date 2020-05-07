import subprocess

def checkProcess(prc = "welle-cli"):
    """Starts Bash command and checks whether that process is running."""
    # Check how many processes with name welle-cli are running
    # Note that when starting process ps fx, total 3 and more processes are found
    p = subprocess.Popen("ps fx | grep " + prc, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    out = p.communicate()[0].splitlines()

    if len(out) < 3:
        # Process is not running
        return False
    else:
        return True

print(checkProcess())