const hbllDevServer = require('@byuhbll/hbll-dev-server');

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
    stats: { timings: true, chunks: false, modules: false },
    devServer: hbllDevServer({
        port: 8888,
        django: {
            port: 18888,
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
