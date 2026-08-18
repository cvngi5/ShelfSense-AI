import time
from detect import detect_objects

image_path = "uploads/images.jpeg"

start = time.time()
result = detect_objects(image_path)

end = time.time()

print("\nRESULTS:")
print(result)

print("\nTIME TAKEN:", round(end - start, 2), "seconds")