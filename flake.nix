{
  description = "flake.nix for QwicClick-Server";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      PORT = "3300";
    in
    {
      packages.${system}.default = pkgs.stdenv.mkDerivation {
        pname = "qwic-click-server";
        version = "0.0.1";
        description = "The QwicClick Redirection and API server";

        src = ./.;

        inherit PORT;

        buildInputs = with pkgs; [
          python311
        ];

        installPhase = ''
          mkdir -p $out/bin
          cp $src/server.py $out/bin/qwic-click-server
          chmod +x $out/bin/qwic-click-server
        '';
      };

      devShells.${system}.default = pkgs.mkShell {
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
        inherit PORT;
      };
    };
}
