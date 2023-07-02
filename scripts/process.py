# Script for data processing
import os
import shutil
import argparse
from sklearn.model_selection import train_test_split # for data splitting

# list all files in a directory
def list_file(dir):
    all_files = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files
    

def process(args):
    # Validate arguments
    if args.source is None:
        raise Exception("Source directory not specified")
    if args.dest_train is None:
        raise Exception("Destination train directory not specified")
    if args.dest_test is None:
        raise Exception("Destination test directory not specified")
    if args.ratio is None:
        raise Exception("Train test split ratio not specified")
    if args.ratio < 0 or args.ratio > 1:
        raise Exception("Train test split ratio should be between 0 and 1")
    
    # Create destination directories and corresponding sub-directories if not exists
    if not os.path.exists(args.dest_train):
        os.makedirs(args.dest_train, exist_ok=True)
    if not os.path.exists(args.dest_test):
        os.makedirs(args.dest_test, exist_ok=True)
    pieces = [f.name for f in os.scandir(args.source) if f.is_dir()]
    for piece in pieces:
        piece_path = os.path.join(args.source, piece)
        train_piece_path = os.path.join(args.dest_train, piece)
        test_piece_path = os.path.join(args.dest_test, piece)
        if not os.path.exists(train_piece_path):
            os.makedirs(train_piece_path, exist_ok=True)
        if not os.path.exists(test_piece_path):
            os.makedirs(test_piece_path, exist_ok=True)
        
        # Split data into train and test sets and copy them to destination directories
        dirs = [f.name for f in os.scandir(piece_path) if f.is_file()]
        train_dirs, test_dirs = train_test_split(dirs, test_size=1-args.ratio, random_state=561)
        
        for dir in train_dirs:
            src = os.path.join(piece_path, dir)
            dst = os.path.join(train_piece_path, dir)
            shutil.copy(src, dst)
        
        for dir in test_dirs:
            src = os.path.join(piece_path, dir)
            dst = os.path.join(test_piece_path, dir)
            shutil.copy(src, dst)
        
        print(f"Train-test split completed for piece {piece}")

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Processing dataset by splitting dataset into train and test sets",
        epilog="Example usage: python scripts/process.py --source ./data --dest-train ./train_data --dest-test ./test_data --ratio 0.8"
    )
    parser.add_argument('--source', type=str, default='data', help='Path to source data directory')
    parser.add_argument('--dest-train', type=str, default='train_data', help='Path to destination train data directory')
    parser.add_argument('--dest-test', type=str, default='test_data', help='Path to destination test data directory')
    parser.add_argument('--ratio', type=float, default=0.8, help='Train test split ratio to be used for training, default 0.8')
    args = parser.parse_args()
    process(args)