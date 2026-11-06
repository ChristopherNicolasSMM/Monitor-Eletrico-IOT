"""Inicialização controlada do portal; Python 3.13 é obrigatório nesta fase."""
import sys

def main():
    if sys.version_info[:2] != (3, 13):
        print(
            f"Python incompatível: {sys.version.split()[0]}. "
            "Utilize Python 3.13.x conforme .python-version e pyproject.toml.",
            file=sys.stderr,
        )
        return 2
    try:
        import uvicorn
    except ModuleNotFoundError:
        print("Dependências ausentes. Execute: python -m pip install -r portal/requirements.txt",file=sys.stderr)
        return 3
    uvicorn.run("portal.app:app", host="127.0.0.1", port=8080, reload=False)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
