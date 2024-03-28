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


def val(params: dict):
    model = YOLO(params['model'])
    return model.val(data=params['data'],
                     imgsz=params['imgsz'],
                     batch=params['batch'],
                     conf=params['conf'],
                     iou=params['iou'],
                     max_det=params['max_det'],
                     device=params['device'],
                     split='test')


def predict(params: dict):
    model = YOLO(params['model'])
    return model.predict(source=params['source'],
                         conf=params['conf'],
                         iou=params['iou'],
                         device=params['device'],
                         max_det=params['max_det'],
                         save=True)
