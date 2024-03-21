from app.minifier import minify


with open("flutter_app/build/web/main.dart.js", "r") as f:
    a = f.read()

origin_len = len(a)

a = minify(a)

with open("output.js", "w") as f:
    f.write(a)

final_len = len(a)


print(f"Original length : {origin_len}")
print(f"Final length : {final_len}")
print(f"Saved : {final_len - origin_len}")
print(f"{(final_len - origin_len)/origin_len*100:.2f}%")
