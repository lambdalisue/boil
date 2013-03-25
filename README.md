boil -- A static Web build tool.
===============================================================================

boil is a tool for building static WEB powered by Jinja2.

Install
-------------------------------------------------------------------------------
Use pip or easy_install like

  pip install boil

Usage
-------------------------------------------------------------------------------

1.  Create `boil.yaml` as below

      source_directory: template
      destination_directory: www
      patterns:
        *.html
      ignore_patterns:
        base.html
        *_base.html
      ignore_directories: False
      case_sensitive: False
      verbose: True
      watch: True

2.  Create Jinja2 template in `template` directory
3.  Run `boil` in root directory

