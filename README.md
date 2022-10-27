# wv_cdm_api

[![forthebadge](https://forthebadge.com/images/badges/built-by-neckbeards.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/designed-in-ms-paint.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
![GitHub forks](https://img.shields.io/github/forks/GetWVKeys/wv_cdm_api?style=for-the-badge)
![GitHub Repo stars](https://img.shields.io/github/stars/GetWVKeys/wv_cdm_api?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/GetWVKeys/wv_cdm_api?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/GetWVKeys/wv_cdm_api.svg?style=plastic)
[![Discord Server](https://discordapp.com/api/guilds/948675767754174465/embed.png)](https://discord.gg/UEt4R3nPJN)
![GitHub issues](https://img.shields.io/github/issues/GetWVKeys/wv_cdm_api.svg?style=plastic)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/GetWVKeys/wv_cdm_api.svg?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/GetWVKeys/wv_cdm_api.svg?style=plastic)

WIP Remote Widevine CDM API

- Certain files are intentionally removed such as devices and wv_cvt, find them on your own if you want them.
- `Visual C++ Redistributable Packages for Visual Studio 2013` is required for wv_cvt.

# setup

- `poetry config virtualenvs.in-project true`
- `poetry install`
- copy `config.example.toml` to `config.toml` and edit as desired
- `poetry run serve` to start development server or `poetry run waitress` to run in production.
