import subprocess


def main():
    try:
        # Ejecutar alembic upgrade head
        subprocess.run(["alembic", "upgrade", "head"], check=True)

        # Ejecutar uvicorn
        subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
