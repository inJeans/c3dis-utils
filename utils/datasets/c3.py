import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

from sklearn.utils.random import sample_without_replacement
from sklearn.model_selection import train_test_split

from utils.datasets import ROOT_DATA_DIR, GDRIVE_DATA_ID

import numpy as np

DEFAULT_NUMBER_POINTS = 3000
DEFAULT_TEST_SIZE = 0.2

def load_data(number_of_points=DEFAULT_NUMBER_POINTS,
              test_size=DEFAULT_TEST_SIZE,
              seed=None):
    if number_of_points > 50000:
        raise Exception("""Sorry we do not have that much data,
                           number_of_points should not exceed 50000""")

    crystal_path = os.path.join(ROOT_DATA_DIR, "crystals.npy")
    clear_path = os.path.join(ROOT_DATA_DIR, "clear.npy")

    if os.path.isfile(crystal_path):
        _get_data("crystals.npy")
    crystal_array = np.load(crystal_path)
    crystal_target = np.ones(crystal_array.shape[0])

    if os.path.isfile(clear_path):
        _get_data("clear.npy")
    clear_array = np.load(clear_path)
    clear_target = np.zeros(clear_array.shape[0])

    data_array = np.vstack((crystal_array, clear_array))
    target_array = np.hstack((crystal_target, clear_target))

    print("Sub-sampling dataset...")
    indices = sample_without_replacement(n_population=data_array.shape[0],
                                         n_samples=number_of_points,
                                         random_state=seed)
    subsampled_data = data_array[indices]
    subsampled_target = target_array[indices]

    print("... shuffling and splitting")
    X_train, X_test, y_train, y_test = train_test_split(subsampled_data, subsampled_target,
                                                        test_size=test_size,
                                                        random_state=seed,
                                                        shuffle=True)
    print("... done")

    return (X_train, y_train), (X_test, y_test)

def _get_data(filename=None):
    # 1. Authenticate and create the PyDrive client.
    auth.authenticate_user()
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials.get_application_default()
    drive = GoogleDrive(gauth)

    # 2. Auto-iterate using the query syntax
    file_list = drive.ListFile(
        {"q": "'{}' in parents".format(GDRIVE_DATA_ID)}).GetList()

    for f in file_list:
        # 3. Create & download by id.
        if filename == None:
            _download_data(drive, f["title"], f["id"])
        elif f['title'] == filename:
            _download_data(drive, f["title"], f["id"])
            

def _download_data(drive, filename, id):
    fname = os.path.join(ROOT_DATA_DIR, filename)
    print("Downloading datafile to {}...".format(fname))
    f_ = drive.CreateFile({'id': id})
    f_.GetContentFile(fname)
    print(".., done")
