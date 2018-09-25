const { spawn } = require('child_process');

const autoprefixer = require('gulp-autoprefixer');
const del = require('del');
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');

// [task] clean
gulp.task('clean', done => {
    del.sync(['./core/static/**/*']);
    done();
});

// [task] copy
gulp.task('copy', () => gulp.src('./assets/img/**/*').pipe(gulp.dest('./core/static/img/')));

// [task] copy:watch
gulp.task('copy:watch', () => gulp.watch('./assets/img/**/*', gulp.series('copy')));

// [task] sass
gulp.task('sass', () =>
    gulp
        .src('./assets/scss/**/*.scss')
        .pipe(sass({ sourceMap: true, outputStyle: 'compressed' }))
        .on('error', error => console.error(error))
        .pipe(sourcemaps.init())
        .pipe(autoprefixer())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('./core/static/css/'))
);

// [task] sass:watch
gulp.task('sass:watch', () => gulp.watch('./assets/scss/**/*.scss', gulp.series('sass')));

// [task] js
gulp.task('js', done => {
    const webpack = spawn('npm', ['run', 'js'], { stdio: 'inherit' });
    webpack.on('exit', () => done());
});

// [task] js:watch
gulp.task('js:watch', () => gulp.watch('./assets/js/**/*.+(js|jsx|ts|tsx)', gulp.series('js')));

// [task] server
gulp.task('server', () => spawn('npm', ['run', 'server'], { stdio: 'inherit' }));

// [task] build
gulp.task('build', gulp.series('clean', gulp.parallel('js', 'sass', 'copy')));

// [task] watch
gulp.task('watch', gulp.series('clean', gulp.parallel('server', 'sass:watch', 'sass', 'copy:watch', 'copy')));
