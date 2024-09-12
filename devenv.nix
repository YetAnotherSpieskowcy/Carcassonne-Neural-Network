{ pkgs, ... }:
{
  packages = [ pkgs.git pkgs.gnumake ];
  languages = {
    python = {
      enable = true;
      package = pkgs.python312;
      venv.enable = true;
      venv.requirements = ./requirements.txt;
    };
    go = {
      enable = true;
      package = pkgs.go_1_22;
    };
  };
}
