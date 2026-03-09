# PicoWord

Password manager with AES encryption, built with Python and CustomTkinter.

## Features

- Master password with PBKDF2-SHA256 hashing
- AES (Fernet) encryption for stored passwords
- CSV import with duplicate detection
- Automatic migration from legacy plain-text format
- Minimal dark UI

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## License

MIT - Developed by [MatPicolli](https://github.com/MatPicolli)
