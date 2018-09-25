# room_reservation
this is a practice app

## Instruction for working on this project

### Project development environment setup

Follow these steps to setup your development environment:

1. Clone the repository. Run
   `git clone git@bitbucket.org:byuhbll/room_reservation.git`.
2. From within the newly created repository directory, create a virtualenv.
   Run `cd room_reservation && python -m venv venv` (or
   create a virtualenv in your favorite way).
3. Activate virtualenv. Run `source venv/bin/activate` (or activate the
   virtualenv in the way that you like activating virtualenvs).
4. Source the project setup script, `source bin/project-setup.sh`. NOTE: this script
   should be modified as the setup for this specific project changes.
8. Contribute!

### Testing in this project

Run the projects tests with `RUNNING_TESTS=true python manage.py test`.
There is an alias for that, `test`. That command will run the tests
in your current virtualenv. To run the tests with a brand new environment
in the targeted environment run `tox` or `tox -r`. This is the prefered way
to run tests.

#### Testing in SemaphoreCI

This project's tests should be setup on SemaphoreCI at [https://semaphoreci.com/byuhbll/room_reservation](https://semaphoreci.com/byuhbll/room_reservation).

The setup step command should be: `cp config.example.yml config.yml && pip install tox`

The test command should be: `tox`

### Deploying this project

The config repository for this project is at 
[https://bitbucket.org/byuhbll/room_reservation/](https://bitbucket.org/byuhbll/room_reservation/). Instructions
for deploying this project can be found in that repositories `README.md` file.

### Frontend Build Process

The tasks that come bundled as part of this project template assist in automating many development
related tasks such as converting `scss` files to `css`, or transpiling modern multi-file
JavaScript into browser-ready single file bundles, as well as automatically reloading your browser
or rerunning your unit tests when a relevant file has been modified. You can also add your own
tasks that are unique to your specific project.

To run a task, `cd` in to your project's root directory and run the following:

`$ npm run <task_name>`

To modify which files and folders are watched/modified/built by each task, modify the scripts
options in your package.json.

#### Prerequisites

In order for all the included tasks to work fully, you need to have Node.js > 8.9.0 installed
and `python2` in your path; you'll need the most recent version of npm installed globally (`$ npm
install -g npm@latest`) and have the project's Node.js dependencies installed into the project's
`node_modules` folder (`$ cd [project_root] && npm install`).

#### Task Reference

##### clean

Deletes files and directories matching the specified files and directories.

##### server

Runs the Webpack dev server while also routing requests as well as the Django dev server and
browsersync. This speeds up the development build process, serving dev versions of js bundle
files from memory such that they are never written to disk, and enables the use of various helpful
development tooling, such as hot module reloading.

##### js

Builds production ready, minified JavaScript bundles.

##### js:watch

Runs the "js" task whenever one of the specified JavaScript files in the project is modified.

##### sass

Build scss files into production ready, minified css.

##### sass:watch

Runs the "sass" task whenever one of the specified scss file in the project is modified.

##### copy

Copies specified files to specified destinations, unchanged.

##### copy:watch

Runs the "copy" task whenever one of the specified files is modified.

##### build

Runs all production build tasks.

##### start

Runs all watch tasks as well as the server task.


#### Upgrading from Old Gulp Setup

* Replace your `webpack.config.js` with this one (be sure to replace `{{app_port}}` and `{{django_port}}` placeholders:

```js
module.exports = {
    entry: { app: './assets/js/index.js' },
    output: {
        path: `${__dirname}/core/static/js`,
        publicPath: '/static/js/',
        filename: '[name].js',
    },
    resolve: {
        extensions: ['.ts', '.tsx', '.js', '.jsx'],
    },
    module: {
        rules: [{ test: /\.[tj]sx?$/, loader: 'ts-loader', exclude: /node_modules/ }],
    },
    devServer: hbllDevServer({
        port: {{app_port}},
        django: {
            port: {{django_port}},
            restartPatterns: ['./**/*.py', './config.yml', '!node_modules'],
            useRunserverPlus: true,
        },
        browsersync: {
            files: [
                './core/static/css/**/*.css',
                './core/static/img/**/*',
                './templates/**/*.html',
            ],
        },
        stats: { timings: true, chunks: false, modules: false },
    }),
};
```

* Replace the three previous js bundles in /templates/_base.html with `<script src="{% static 'js/app.js' %}" type="text/javascript"></script>`
* Delete `gulpfile.js`
* Remove the following dependencies from `package.json`
  * `@byuhbll/gulp-dev-server`
  * `@types/gulp`
  * `awesome-typescript-loader`
  * `case-sensitive-paths-webpack-plugin`
  * `gulp-concat`
  * `gulp-notify`
  * `uglifyjs-webpack-plugin`
  * `yargs`
* Add / update (to the latest) the following dependencies in `package.json`:
  * `@byuhbll/hbll-dev-server`
  * `ts-jest`
  * `ts-loader`
  * `ts-node`
  * `tsutils`
  * `typescript`
  * `webpack`
  * `webpack-cli`
  * `webpack-dev-server`

Look at the pull request that merged these changes for more detailed info: https://bitbucket.org/byuhbll/django-project-template/pull-requests/18/switch-to-npm-scripts-and-webpack-dev/diff

