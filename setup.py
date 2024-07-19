from distutils.core import setup
setup(
  name = 'QiRub',         # How you named your package folder (MyLib)
  packages = ['QiRub'],   # Chose the same as "name"
  version = '1.0.9',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Rubka Client Library',   # Give a short description about your library
  author = 'Host1let',                   # Type in your name
  author_email = 'sqlmapssh@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Rubier-Project/QiRub',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Rubier-Project/QiRub/archive/refs/heads/main.zip',    # I explain this later on
  keywords = ['qirubika'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          "httpx",
          "pycryptodome",
          "fake_useragent",
          "rich",
          "Pillow",
          "mutagen"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11'
  ],
)
