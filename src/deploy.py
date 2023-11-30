import os


print("The deploy script has started successfully!\n")

print("Environment variables:")
environ_keys = sorted(dict(os.environ).keys())
environ_maxlen = max([len(x) for x in environ_keys])

for k in environ_keys:
    print(f"    {k:{environ_maxlen}s} : {os.environ[k]}")

print()

print("The deploy task finished.")
exit(0)
