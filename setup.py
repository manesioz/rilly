from setuptools import setup, Extension
  
setup(
  name = 'rilly',         
  packages = ['rilly'],  
  version = '0.1.0',      
  license='MIT',        
  description = 'Change Data Capture Python library for BigQuery',   
  author = 'Zachary Manesiotis',        
  author_email = 'zack.manesiotis@gmail.com',    
  url = 'https://github.com/manesioz/rilly',   
  download_url = 'https://github.com/manesioz/rilly/archive/v0.1.0.tar.gz',    
  keywords = ['chn=ange-data-capture', 'python', 'bigquery', 'kafka', 'pubsub', 'distributed-system'],   
  install_requires=[
          'google-cloud-pubsub',
          'google-cloud-logging', 
          'faust[rocksdb,uvloop,fast,redis]',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)