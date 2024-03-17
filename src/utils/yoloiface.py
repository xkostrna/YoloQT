from ultralytics import YOLO


def train(params: dict):
    model = YOLO(params['model'])
    return model.train(data=params['data'],
                       imgsz=params['imgsz'],
                       patience=params['patience'],
                       epochs=params['epochs'],
                       batch=params['batch'],
                       save_period=params['save_period'],
                       device=params['device'],
                       workers=params['workers'],
                       optimizer=params['optimizer'],
                       verbose=True)
