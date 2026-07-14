import os
import time
import shutil
from pathlib import Path
from pipeline import run_pipeline
import output_inpainting as inp

# 1. Загружаем модели ОДИН РАЗ
print("--- [Worker] Загрузка моделей в GPU (это надолго)... ---")
device = "cuda"
cfg = inp.CFG
pipe = inp.build_pipeline(device, cfg) 
print("--- [Worker] Модели загружены, система готова! ---")

def process_queue():
    queue_dir = Path("data/queue")
    out_dir = Path("data/outputs")
    queue_dir.mkdir(exist_ok=True)
    
    while True:
        # Ищем задачи
        tasks = list(queue_dir.glob("*.jpg")) + list(queue_dir.glob("*.png"))
        for task in tasks:
            print(f"[{time.ctime()}] Начало обработки: {task.name}")
            try:
                # Передаем уже загруженный pipe, чтобы не ждать 7 минут
                run_pipeline(image=task, client="data/clients/ivan.jpg", seeds=5)
                # Перемещаем обработанный файл в папку, чтобы он не крутился по кругу
                shutil.move(str(task), str(queue_dir / "processed" / task.name))
            except Exception as e:
                print(f"Ошибка при обработке {task.name}: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    process_queue()
