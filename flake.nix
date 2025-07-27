{
  description = "flake.nix for QwicClick-Server Environment";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShell {
        name = "QwC";
        buildInputs = with pkgs; [
          virtualenv
          python311
        ];
        shellHook = ''
          export VIRTUAL_ENV_DISABLE_PROMPT=1
          virtualenv venv -q
          source ./venv/bin/activate
        '';
        PORT = "3300";
      };
    };
}
