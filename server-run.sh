#!/usr/bin/env sh
is_root () {
    return $(id -u)
}

has_sudo() {
    local prompt

    prompt=$(sudo -nv 2>&1)
    if [ $? -eq 0 ]; then
    echo "has_sudo__pass_set"
    elif echo $prompt | grep -q '^sudo:'; then
    echo "has_sudo__needs_pass"
    else
    echo "no_sudo"
    fi
}

elevate_cmd () {
    local cmd=$@

    HAS_SUDO=$(has_sudo)

    case "$HAS_SUDO" in
    has_sudo__pass_set)
        sudo $cmd
        ;;
    has_sudo__needs_pass)
        echo "Please supply sudo password for the following command: sudo $cmd"
        sudo $cmd
        ;;
    *)
        echo "No sudo access, please contact the system administrator."
        exit 1
        ;;
    esac
}

if is_root; then
    echo "Error: need to call this script as a normal user, not as root!"
    exit 1
fi
elevate_cmd podman pod exists tt
if [$? -eq 0]; then
    elevate_cmd podman play kube --down tt.yaml
fi

elevate_cmd sudo podman --runtime /usr/bin/crun play kube --build tt.yaml