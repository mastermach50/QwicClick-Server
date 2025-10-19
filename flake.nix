{
  description = "flake.nix for QwicClick-Server";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      PORT = "3300";

      pythonEnv = pkgs.python312.withPackages (p: with p; [
        pymysql
        bcrypt
      ]);
    in
    {
      packages.${system}.default = pkgs.stdenv.mkDerivation {
        pname = "qwic-click-server";
        version = "0.0.1";
        description = "The QwicClick Redirection and API server";

        src = ./.;

        inherit PORT;

        nativeBuildInputs = [ pkgs.makeWrapper ];

        dontBuild = true;

        installPhase = ''
          mkdir -p $out/bin $out/libexec/qwic-click-server
          cp -R $src/src/* $out/libexec/qwic-click-server
          makeWrapper ${pythonEnv}/bin/python $out/bin/qwic-click-server \
            --set PYTHONPATH "$PYTHONPATH:$out/libexec/qwic-click-server" \
            --add-flags "$out/libexec/qwic-click-server/main.py"
        '';
      };

      devShells.${system}.default = pkgs.mkShell {
        name = "QwC";
        buildInputs = with pkgs; [
          python312
        ];
        VIRTUAL_ENV_DISABLE_PROMPT = 1;
        shellHook = ''
          uv venv --no-managed-python --python python312 --allow-existing
          source ./.venv/bin/activate
        '';
        inherit PORT;
      };
    };
}
