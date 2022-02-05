from setuptools import setup

setup(name='AWSLoginGuard',
      version='0.0.1',
      description='Keep an eye on the AWS login activities',
      url='https://github.axa.com/marvin-kraus/cb-auto-patcher',
      author='Der Benji',
      author_email='nyctophobia@protonmail.com',
      license='MIT Licence',
      packages=['aws-loginguard'],
      setup_requires=[
          'wheel',
      ],
      install_requires=[
          'botocore',
          'boto3'
      ],
      python_requires='>=3.8',
      zip_safe=True)
