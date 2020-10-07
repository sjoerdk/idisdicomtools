from idisdicomtools.cstore import CStoreNode

node = CStoreNode(port=11112, storage_root='/tmp/pynettest')
node.start()

"""
Now, in a separate terminal, try something like this (with dcmtk standard tools
installed:

$ echoscu localhost 11112
$ storescu localhost 11112 -aet project1 <idisdicomtools>/examples/resources/a_dicom_file
"""
