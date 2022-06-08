#!/bin/sh

# install python dependencies
pipenv install

# check nodejs
node --version

# check canvas install prerequisites
# sudo yum install gcc-c++ cairo-devel libjpeg-turbo-devel pango-devel giflib-devel

# install node_modules
npm --prefix ticketscraping/js ci