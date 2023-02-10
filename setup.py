from setuptools import setup
from distutils.command.build_py import build_py

class ProtobufGen(build_py):
    def run(self):
        import os
        
        os.system('protoc proto/messages.proto --python_out=.')

        build_py.run(self)

setup(
    name='protobuf_parser',
    version='1.0.0',
    description='Разбор потока length-prefixed Protobuf сообщений на Python',
    long_description="",
    zip_safe=False,
    packages=['protobuf_parser', 'proto'],
    cmdclass={'build_py': ProtobufGen},
)