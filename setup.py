from setuptools import setup, find_packages

import udevedu


if __name__ == '__main__':
    setup(
        name='udevedu',
        description='udev event dispatcher for unpriviledged user',
        long_description=udevedu.__doc__,
        version=udevedu.__version__,
        license='BSD 2-clause',
        packages=find_packages(),
        install_requires=[
            'pyudev',
            'pyxdg',
        ],
        entry_points=dict(
            console_scripts=['udevedu = udevedu:main']
        )
    )
