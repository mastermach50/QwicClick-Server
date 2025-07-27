# shell.nix for QwicClick-Server Environment
{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  name = "QwC";
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
  PORT = "3300";
}
