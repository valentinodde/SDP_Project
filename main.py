from create_model import create_staff_qualifications
from data_loader import load_small_data

if __name__ == '__main__':
    print(create_staff_qualifications(load_small_data()))