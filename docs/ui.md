## yarn

theme/package.json:

~~~json
{
  "dependencies": {
    "axios": "^0.16.2",
    "bootstrap": "^3.3.7",
    "jquery": "^3.2.1",
    "lodash": "^4.17.4",
    "underscore": "^1.8.3",
    "vue": "^2.4.4"
  }
}
~~~

~~~bash
$ cd theme
$ yarn install
$ mkdir static && cd static
$ ln -s ../node_modules lib
~~~
