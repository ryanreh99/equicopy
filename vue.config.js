module.exports = {
  publicPath: './',
  outputDir: './dist/',
  // Relative imports are nested twice and django collectstatic
  // nests only 1 directory, so we add 2 directories instead.
  assetsDir: "static/static"
}