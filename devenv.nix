{ pkgs, ... }:
{
  packages = [ pkgs.git pkgs.gnumake ];
  languages = {
    python = {
      enable = true;
      package = pkgs.python312;
      venv.enable = true;
      venv.requirements = ./requirements-dev.txt;
    };
    go = {
      enable = true;
      package = pkgs.go_1_22;
    };
  };
  scripts.style.exec = ''
    ${pkgs.ruff}/bin/ruff check src test
    ${pkgs.ruff}/bin/ruff format src test
    '';
}
