# shell.nix for Python Environment
{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  name = "Py";
  packages = with pkgs; [
    virtualenv

    (python311.withPackages (python-pkgs: [
      python-pkgs.pip
    ]))

  ];
  shellHook = ''
    export VIRTUAL_ENV_DISABLE_PROMPT=1
    virtualenv venv -q
    source ./venv/bin/activate
  '';
}
