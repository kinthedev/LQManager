def copy_to_clipboard(root, text: str):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

def mask_password(password: str) -> str:
    return '••••••••'

def format_number(n: int) -> str:
    return f"{n:,}"
