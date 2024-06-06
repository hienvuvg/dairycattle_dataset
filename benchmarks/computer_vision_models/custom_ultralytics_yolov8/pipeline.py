from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Train the model with 2 GPUs
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device="mps")
"""
import ultralytics
import time
import torch
import argparse

def main():
    model = ultralytics.YOLO(args.yolov8_path)
    # data_path = '/nfs/oprabhune/MmCows/vision_data/unlabeled_data/0721/images/0721/cam_1'
    # data_path = '/nfs/oprabhune/MmCows/vision_data/detection/organized_data/fold_1/train/images/cam_1_1690271846_02-57-26.jpg'
    #data_path = '/nfs/oprabhune/MmCows/vision_data/detection/organized_data/fold_1/train/images/cam_1_1690272821_03-13-41.jpg'
    # data_path = '/nfs/oprabhune/MmCows/vision_data/detection/organized_data/fold_1/test/images'
    # data_path = '/nfs/oprabhune/MmCows/dummy_data_2/cam_3_1690347416_23-56-56.jpg'
    # data_path = '/nfs/oprabhune/MmCows/vision_data/detection/organized_data/fold_1/test/images/cam_1_1690321016_16-36-56.jpg'
    start_time = time.time()
    results = model.predict(
        args.data_path,
        #  device = 'cpu',
        # show = True,
        # save = True,
        # save_txt  =True,
        # save_crop = True
        )

    print('\nTime taken: ', time.time() - start_time)

if __name__ == "__main__":
    # Argument parser
    if torch.cuda.is_available():
        device = torch.device("cuda")

    if torch.backends.mps.is_available():
        device = torch.device("mps")

    else:
        device = torch.device("cpu")
    parser = argparse.ArgumentParser(description='Inference Pipeline')
    parser.add_argument('--data_path', type=str, required=True, help='Path to the data directory containing images to be inferred')
    parser.add_argument('--yolov8_path', type=str, default = '/Users/omkar/Library/CloudStorage/OneDrive-purdue.edu/Omkar_research/CPS_dataset/benchmarking/yolov8_cow_detector.pt')
    args = parser.parse_args()
    main()
"""