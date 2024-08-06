import sys
print(sys.executable)

try:
    import wtforms
    print("WTForms is installed.")
except ImportError:
    print("WTForms is not installed.")