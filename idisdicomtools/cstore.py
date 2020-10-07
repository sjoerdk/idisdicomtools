"""Classes and functions implementing a DICOM C-store dicom node.
A host:port that you can send DICOM files to
"""

from pathlib import Path

from pynetdicom import (
    AE, evt,
    StoragePresentationContexts,
    PYNETDICOM_IMPLEMENTATION_UID,
    PYNETDICOM_IMPLEMENTATION_VERSION
)


class CStoreNode:

    def __init__(self, port: int, storage_root: str):
        """A DICOM C-store node which stores according to aet
        Parameters
        ----------
        port: int
            listen for incoming C-store requests on this port
        storage_root: str
            save incoming files to this path. Will create path if it does not exist
        """
        self.port = port
        self.storage_root = Path(storage_root)
        self.active = False

    def start(self):
        """Start listening for incoming files
        Notes
        -----
        This method will not return. Has to be stopped with break
        """
        print(f"Will save incoming data to:")
        print(f"{self.storage_root}/<aet>/SeriesInstanceUID/SopInstanceUID")
        print("Starting DICOM node... press ctrl-C to stop")

        handlers = [(evt.EVT_C_STORE, self.handle_store)]

        # Initialise the Application Entity
        ae = AE()

        # Add the supported presentation contexts
        ae.supported_contexts = StoragePresentationContexts

        # Start listening for incoming association requests
        ae.start_server(('', self.port), evt_handlers=handlers)

    def handle_store(self, event):
        """Handle a C-STORE request event."""
        try:
            # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
            ds = event.dataset

            # Add the File Meta Information
            ds.file_meta = event.file_meta

            # Save the dataset using the SOP Instance UID as the filename
            aet = event.assoc.remote['ae_title'].decode('utf-8').rstrip()
            filepath = self.storage_root / aet / event.dataset.StudyInstanceUID / \
                       ds.SOPInstanceUID

            print(f"saving to '{filepath}'")
            filepath.parent.mkdir(parents=True, exist_ok=True)
            ds.save_as(str(filepath), write_like_original=False)

            # Return a 'Success' status
            return 0x0000
        except Exception as e:
            print(e)
            raise  # TODO: investigate sending non-success statuses
